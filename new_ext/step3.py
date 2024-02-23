# Open the file

def extend_lists(dicts_to_merge):
    merged_output = {}
    # dicts_to_merge = [samp_out1, samp_out2, samp_out3]
    for d in dicts_to_merge:
        for key, value in d.items():
            if key not in merged_output:
                merged_output[key] = []
            merged_output[key].extend(value)
    return(merged_output)


dict_li=[]
with open('/Users/sathishkumar/AllFiles/vegavega/prop_arch/external_ids/output/output2.txt', 'r') as file:
    # Read each line
    for line in file:
        # Convert line to dictionary using eval()
        data = eval(line)
        dict_li.append(data)

res=extend_lists(dict_li)

print(res)

# handle_raw_dict
