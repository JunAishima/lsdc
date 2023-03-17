
def standard(reqObj):

    logger.info("moving omega to start " + str(time.time()))
    if daq_utils.beamline == "nyx":
        direction = (sweep_end - sweep_start) / abs(sweep_end - sweep_start)
        beamline_lib.mvaDescriptor("omega",sweep_start - direction*0.05)
    else:
        beamline_lib.mvaDescriptor("omega",sweep_start)
    collect_detector_seq_hw(sweep_start,range_degrees,img_width,exposure_period,file_prefix,data_directory_name,file_number_start,currentRequest)
    send_kafka_message(topic=f'{daq_utils.beamline}.lsdc.documents', event='stop', uuid=currentRequest['uid'], protocol=reqObj["protocol"])
    standard_processing(reqObj)

def standard_processing(reqObj):
    seqNum = flyer.detector.cam.sequence_id.get()
    comm_s = os.environ["LSDCHOME"] + "/runSpotFinder4syncW.py " + data_directory_name + " " + file_prefix + " " + str(currentRequest["uid"]) + " " + str(seqNum) + " " + str(currentIspybDCID)+ "&"
    logger.info(comm_s)
    os.system(comm_s)
    if img_width > 0: #no dataset processing in stills mode
        if (reqObj["fastDP"]):
            if (reqObj["fastEP"]):
                fastEPFlag = 1
            else:
                fastEPFlag = 0
            if (reqObj["dimple"]):
                dimpleFlag = 1
            else:
                dimpleFlag = 0
            nodeName = "fastDPNode" + str((fastDPNodeCounter%fastDPNodeCount)+1)
            fastDPNodeCounter+=1
            node = getBlConfig(nodeName)
            dimpleNode = getBlConfig("dimpleNode")
            if (daq_utils.detector_id == "EIGER-16"):
                seqNum = flyer.detector.cam.sequence_id.get()
                comm_s = os.environ["LSDCHOME"] + "/runFastDPH5.py " + data_directory_name + " " + str(seqNum) + " " + str(currentRequest["uid"]) + " " + str(fastEPFlag) + " " + node + " " + str(dimpleFlag) + " " + dimpleNode + " " + str(currentIspybDCID)+ "&"
            else:
                comm_s = os.environ["LSDCHOME"] + "/runFastDP.py " + data_directory_name + " " + file_prefix + " " + str(file_number_start) + " " + str(int(round(range_degrees/img_width))) + " " + str(currentRequest["uid"]) + " " + str(fastEPFlag) + " " + node + " " + str(dimpleFlag) + " " + dimpleNode + "&"
            logger.info(f'Running fastdp command: {comm_s}')
            if (daq_utils.beamline in ("amx", "fmx")):
                visitName = daq_utils.getVisitName()
            if (not os.path.exists(visitName + "/fast_dp_dir")) or subprocess.run(['pgrep', '-f', 'loop-fdp-dple-populate'], stdout=subprocess.PIPE).returncode == 1:  # for pgrep, return of 1 means string not found
                os.system("killall -KILL loop-fdp-dple-populate")
                logger.info('starting fast dp result gathering script')
                os.system("cd " + visitName + ";${LSDCHOME}/bin/loop-fdp-dple-populate.sh&")
            os.system(comm_s)
            if (reqObj["xia2"]):
                comm_s = f"ssh -q xf17id2-srv1 \"{os.environ['MXPROCESSINGSCRIPTSDIR']}xia2.sh {currentRequest['uid']} \"&"
                os.system(comm_s)
