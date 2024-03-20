## removeRedundantProteins.py
import sys
import getopt

def usage():
    print('用法：python3 removeRedundantProteins.py -i <输入fasta文件> -o <输出fasta文件> <-h>')
    return

def removeRedundant(in_file, out_file):
    gene_dic = {}  
    flag = ''  
    with open(in_file, 'r') as in_fasta:
        for line in in_fasta:
            if '>' in line:
 
                li = line.strip('>\n').split('.')[0]
                flag = li
                try:
                    gene_dic[li]
                except KeyError:
                    gene_dic[li] = [line]
                else:
                    gene_dic[li].append(line)
            else:
                gene_dic[flag][-1] += line  # 

    with open(out_file, 'w') as out_fasta:
        for key, value in gene_dic.items():
            if len(value) == 1: 
                out_fasta.write(gene_dic[key][0])
            else:
                trans_max = '' 
                for trans in gene_dic[key]:
                    if len(trans) > len(trans_max):  
                        trans_max = trans
                out_fasta.write(trans_max) 

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hi:o:')   
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-i':
            in_fasta_name = arg
        elif opt == '-o':
            outfile_name = arg
    try:
        removeRedundant(in_fasta_name, outfile_name)
    except UnboundLocalError:  
        usage()
    return

if __name__ == '__main__':
    main(sys.argv[1:]) 
