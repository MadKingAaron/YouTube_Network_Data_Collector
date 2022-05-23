import glob, os, subprocess, shlex, shutil

folder_name = './CSVs'
def check_if_exists(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

def get_pcaps():
    return [file for file in glob.glob("*.pcap")]

def format_pcap_name(pcap):
    pcap = pcap.replace('.pcap', '')
    new_name =''.join(char for char in pcap if char.isalnum())
    new_name += '.pcap'
    #os.rename(pcap, new_name)
    return new_name

def convert_all_pcaps():
    pcaps = get_pcaps()
    for pcap in pcaps:
        print("Converting '%s' to CSV" %pcap)
        convert_pcap_to_csv(pcap)

def get_csv_file_name(pcap_name:str)->str:
    name = pcap_name.replace('.pcap', '.csv')
    return os.path.join(folder_name, name)

def make_temp_file(pcap:str, tmp_name:str):
    shutil.copy(pcap, tmp_name)

def del_tmp_file(tmp_name:str):
    os.remove(tmp_name)

def convert_pcap_to_csv(pcap:str):
    tmp_file = format_pcap_name(pcap)
    make_temp_file(pcap, tmp_file)

    csv_name = get_csv_file_name(tmp_file)
    cmd = ("tshark -r %s -T fields -e frame.number -e frame.time -e frame.time_relative -e frame.time_delta -e ip.src -e ip.dst -e ip.proto -e frame.len -e frame.protocols -e data.len -E header=y -E separator=, -E quote=d -E occurrence=f > %s" %('./'+tmp_file, csv_name))
    print(cmd)
    os.system(cmd)

    del_tmp_file(tmp_file)

    #subprocess.run(cmd)

if __name__ == '__main__':
    check_if_exists(folder_name)
    convert_all_pcaps()