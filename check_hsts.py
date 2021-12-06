import subprocess
import json

f = open('domain_list.txt')
data = json.load(f)


write = open('output.txt','w')


for dom in data["domains"]:
    domain = dom["domain"]
    x = subprocess.Popen("nmap -p 443 --script http-hsts-verify {} | grep 'HSTS is not configured'".format(domain), shell=True, stdout=subprocess.PIPE)
    exit_code = x.wait()
    write.write("{}:{}\n".format(domain,str(exit_code)))

write.close()



    
