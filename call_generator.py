#!/usr/bin/python3

#import subprocess => run an external program(Bash command in Linux, ex. sipp command)
#import shlex => simple syntax resembling of Unix Shell

import time
import json
import os
import subprocess
import shlex

#read uac_new_num.xml and replace 'new_num' with new_num and generate uac_new_temp.xml file
def set_new_call(new_num):
    with open("uac_new_num.xml",'rt') as fin:
        with open("uac_new_temp.xml", 'wt') as fout:
            for line in fin:
                fout.write(line.replace("new_num", new_num))

                
#uac_loc = r'/vagrant/sipp/call_generator/uac_new_temp.xml'
#get uac_new_temp.xml file
uac_loc = 'uac_new_temp.xml'
sig_address = "10.0.2.15:5060"
#sig_address = "192.168.33.10:5060"
CarrierIPs = {'C0': '192.168.33.11',
              'C1': '192.168.33.12',
              'C2': '192.168.33.13',
              'C3': '192.168.33.14',
              }

DialCodes = [4123, 4323, 4562, 4732, 4123, 4323, 4562, 4732, 4323, 4562]
PhoneNumbers= [292888892, 292888899, 292888877, 292888818 ]

call_duration = 3000
call_number = 1
call_fail = 0
long_str = "#############################################";
extra_long_str = "#########################################################################################################";

results = {}

for j in range(4):
    old_time = time.time()
    for i in range(10):
        carrier_ip = CarrierIPs["C"+ str(j)]
        carrier = "C" + str(j)
        return_msg = "PASS"
        BParty = "0011" + str(DialCodes[i]) + "456789" + str(i)
        AParty = '0' + str(PhoneNumbers[j])
        set_new_call(AParty)
        print(extra_long_str)
        print("Ingress Endpoint = C{}  #### Calling Number = {} #### Dailed Number = {}".format(j, AParty, BParty))
        print("      {}                ".format(call_number))
 
        #sipp_command = ("sipp {} -i {} -sf {} -t un -r 1 -m 1 -s {} -d {} -l 2000 2>&1 | grep Contact:".format(sig_address, carrier_ip, uac_loc, BParty, call_duration ))
        #sipp_command = ['sipp', sig_address, '-sf', uac_loc,'-i',carrier_ip,'-t','un', '-r','1', '-m','1','-s', BParty, '-d', str(call_duration), '-l','2', '2>&1','| grep Contact:']
        # sipp_command = ['sipp', sig_address, '-sf', uac_loc,'-i',carrier_ip,'-t','un', '-r','1', '-m','1','-s', BParty, '-d', str(call_duration), '-l','2', '2','>','&','1','|','grep','Contact:']
        # shlex.split deprecated since 3.9
        # sipp_command = shlex.split("sipp 10.0.2.15 -sf  uac_new_temp.xml -i 192.168.33.11 -t un -r 1 -m 1 -d 3000 -l 2 2>&1 | grep Contact:")
        sipp_command = ['sipp', sig_address, '-sf', uac_loc, '-i', carrier_ip, '-t', 'un', '-r', '1', '-m', '1', '-d', '3000', '-l', '2', '2>&1', '|', 'grep', 'Contact:']


        try:
            #subprocess.run(sipp_command)
            run_sipp = subprocess.Popen(sipp_command)
            run_sipp.wait()
        except subprocess.CalledProcessError as err:
            print('SIPP Command ERROR: ', err)


        finish_time = time.time()
        total_time = finish_time - old_time
        setup_time = total_time - call_duration/1000;


        if (setup_time < 1):
            results[call_number] = {'Stat': "Failed"}
            call_fail +=1
        else:
            if (setup_time < 3 ):
               results[call_number] = {'Stat': "Pass"}

            else:
                results[call_number] = {'Stat': "SETUP"}

        results[call_number]['finish_time'] = finish_time
        results[call_number]['carrier'] = carrier
        results[call_number]['AParty'] = AParty
        results[call_number]['BParty'] = BParty
        results[call_number]['call_duration'] = call_duration/1000
        results[call_number]['setup_time'] = setup_time

        old_time = finish_time
        call_number += 1


with open("results.json", "w") as f:
    #results_json = json.dumps(results)
    #results_json = json.dumps(results, indent=None, separators=(', ', ': '))
    results_json = json.dumps(results, indent=2, separators=(', ', ': '))
    f.write(results_json)
