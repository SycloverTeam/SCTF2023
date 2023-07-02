import hashlib

hashtable = [
'284f3e527b475c0dcbe1a7aed94ce31539131545',
'e4af700f9921ed71c190316cd5564f8ce1303f94',
'b4aa9bc1e62e19828a370c50a4cff71bd9736bb4',
'ad2af979abd26a0a35cca0218f32277d01b7f7d3',
'f9ccf51238cbee2ee8282f28ff1a526a8a39d8e4',
'89b4ebdc6413bec34138a3b63f23671932ea5696',
'9329c7181085b1d6484e4fbc826fb3c25ca25f32',
'ab4400a33c16525c50a2e6dda8c05eacd5b3d7f0',
'386b00cd1573492bf3dd76da57eb73759c7de8e1',
'9de01d0bc2f7b7440b99e96daaf372f93e53b140',
]

dicts={}
flag=''
letter = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_"
for i in letter:
    for j in letter:
        for k in letter:
            for l in letter:
                tmp = i + j + k + l
                hash = hashlib.sha1(tmp.encode(encoding="ascii")).hexdigest()
                if hash in hashtable:
                    dicts[hash]=tmp
                    print(dicts)
                    if len(dicts) == 10:
                        for i in hashtable:
                            flag+=dicts[i]
                        print(flag)
                        exit()