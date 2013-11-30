import matplotlib.pyplot as plt

def get_counts(data):
    return [(i,len(data[i])) for i in data]

def clean_subj(s_data):
    s_data = [i for i in s_data if int(i[1])==0 and \
                int(i[2])>0 and \
                int(i[3])>0 and \
                int(i[4]) >-1] #difficulty
    return s_data

def clean_all(subj_list, subj_data):
    cln_data = {}
    for s in subj_list.keys():
        cln_data[int(s)] = clean_subj(subj_data[int(s)])
    return cln_data

def plot_cleaned_counts(subj_data, cln_data):
    cnt1=get_counts(subj_data)
    cnt2=get_counts(cln_data)

    fig, ax = plt.subplots()

    ax.plot([i[0] for i in cnt1], [i[1] for i in cnt1], "-o", label="original")
    ax.plot([i[0] for i in cnt2], [i[1] for i in cnt2], "-o", label="cleaned")
    plt.xlabel("Id")
    plt.ylabel("Size")
    plt.legend()
    plt.grid()
    plt.title("Comparing original and new size of data")
