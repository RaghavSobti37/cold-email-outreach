"""Minimal MX lookup over UDP (no deps). Returns list of MX hosts or [] ; None on error."""
import socket, struct, random, sys
def _name(buf, off):
    labels=[]; jumped=False; end=None
    while True:
        l=buf[off]
        if l==0: off+=1; break
        if l&0xC0==0xC0:
            ptr=((l&0x3F)<<8)|buf[off+1]
            if not jumped: end=off+2
            off=ptr; jumped=True; continue
        labels.append(buf[off+1:off+1+l].decode(errors='ignore')); off+=1+l
    return '.'.join(labels), (end if jumped else off)
def query(domain, qtype=15, server='8.8.8.8', timeout=4):
    tid=random.randint(0,65535)
    q=struct.pack('>HHHHHH',tid,0x0100,1,0,0,0)
    for p in domain.strip('.').split('.'): q+=bytes([len(p)])+p.encode()
    q+=b'\x00'+struct.pack('>HH',qtype,1)
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.settimeout(timeout)
    try:
        s.sendto(q,(server,53)); buf,_=s.recvfrom(4096)
    except Exception: return None
    finally: s.close()
    _,flags,qd,an,_,_=struct.unpack('>HHHHHH',buf[:12])
    rcode=flags&0xF
    if rcode==3: return []  # NXDOMAIN
    off=12
    for _ in range(qd): _,off=_name(buf,off); off+=4
    out=[]
    for _ in range(an):
        _,off=_name(buf,off); t,_,_,rl=struct.unpack('>HHIH',buf[off:off+10]); off+=10
        if t==15: out.append(_name(buf,off+2)[0])
        elif t==1: out.append('.'.join(map(str,buf[off:off+4])))
        off+=rl
    return out
def mx_ok(domain):
    r=query(domain,15)
    if r is None: r=query(domain,15,'8.8.4.4')
    if r: return True, r
    a=query(domain,1)  # implicit MX via A record
    return bool(a), a or []
if __name__=='__main__':
    for d in sys.argv[1:]: print(d, mx_ok(d))
