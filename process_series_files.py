import sys, os
from os.path import isfile, join
import re
import eegml

# Create dict of machine data
def create_dict_machine_data(raw_dir):
    onlyfiles_raw = [ f for f in os.listdir(raw_dir) if isfile(join(raw_dir,f)) ]
    pat_raw = re.compile("[0-9]*\.[a-z0-9]*\.rawwave\.csv")
    temp_dat_raw = [f.split('.')[0:2] for f in onlyfiles_raw if pat_raw.match(f)]
    mach_dict = {i[1]: i[0] for i in temp_dat_raw}
    return mach_dict

def process_all_in_dir(indir, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    mach_dict = create_dict_machine_data(indir)
    for i in mach_dict:
        file_in = join(indir, mach_dict[i]+"."+i+".rawwave.csv")
        print "processing file %s" % file_in
        file_out =join(outdir, mach_dict[i]+"."+i+".rawwave_microsec.csv")
        eegml.create_raw_incremental(file_in,file_out, mach_dict[i])

if __name__ == '__main__':
    indir,outdir=sys.argv[1:3]
    process_all_in_dir(indir,outdir)
