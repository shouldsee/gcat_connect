prog='gcat_connect.py'

__doc__=f'''
Requires: 
 - docopt==0.6.2
 - sshpass
 - sshfs
 - ssh

Usage:
#  {prog} command --option <argument>
  {prog} --ALIAS=<ALIAS> --PASS=<PASS> --USER=<USER>
--HOST=<HOST>
[--SSH_PORT=<SSH_PORT>]
[--tunnel_mode=<tunnel_mode>]
[--tunnel_port=<tunnel_port>]
[--tunnel_dest_port=<tunnel_dest_port>]
[--source_host=<source_host>]
[--dest_host=<dest_host> ]
[--dry]
[--test]
[--mount]
[--mount_remote_dir=<mount_remote_dir>]
[--verbose]

Options:
  -v/--verbose print executed command
  --SSH_PORT=<SSH_PORT>   port for ssh connection [default: 22]
  --dest_host=<dest_host> Destination host to bind  for SSH tunnel   [default: localhost]
  --tunnel_port=<tunnel_port> Source port to tunnel
  --mount_remote_dir=<mount_remote_dir> Which remote directory to mount  [default: /root/ ]
#  {prog} (--either-that-option | <or-this-argument>)
#  {prog} --another-option=<with-argument>
#  {prog} <repeating-argument> <repeating-argument>...
#  {prog} --test

'''

__doc__ = '\n'.join([x for x in __doc__.splitlines() if not x.strip().startswith('#') ])
from docopt import docopt
import os

def strip_dash(x):
    for k in list(x):
        if k.startswith('-'):
            kk = k.lstrip('-')
            x[kk] = x.pop(k)
    return x

def gcat_main(argv=None):
    print(argv)
    x = docopt(__doc__,argv=argv,options_first=True)
 # argv = [args['<command>']] + args['<args>']
    x = strip_dash(x)
    # print(x)
    # return
    _main(**x)
main = gcat_main

import subprocess
def _main(
    ALIAS,PASS,USER,SSH_PORT,HOST,
    tunnel_mode,source_host,
    dest_host,
    dry,
    tunnel_dest_port,
    tunnel_port,
    mount,
    mount_remote_dir,
    verbose,
    **args):
    _system = os.system
    # _system = lambda x: subprocess.run(x,shell=True)
    print(ALIAS)
    IP=HOST

    '''
    TARGET=default
    while [[ $# -gt 0 ]]; do
      case $1 in
        -t|--tunnel)
          TARGET=tunnel
          FPORTF=$2
          FPORT=$3
          shift # past argument
          shift # past value
          shift
          ;;
        --local)
          IP=192.168.50.132
          SSH_PORT=22
          shift # past argument
          ;;
        -*|--*)
          echo "Unknown option $1"
          exit 1
          ;;
        *)
          POSITIONAL_ARGS+=("$1") # save positional arg
          shift # past argument
          ;;
      esac
    done
    '''
    SSH_ARGS = f'-p {SSH_PORT}'
    SSH_ARGS_EXTRA = '-vvvv'
    if tunnel_mode is not None:
        assert tunnel_port is not None,'Error: tunnel source port not specified'
        if 'D' in tunnel_mode:
            tconf = tunnel_port
        else:
            'LR'
            if tunnel_dest_port is None:
                tunnel_dest_port = tunnel_port
            if source_host is not None:
                tconf = f'{source_host}:{tunnel_port}:{dest_host}:{tunnel_dest_port}'
            else:
                tconf = f'{tunnel_port}:{dest_host}:{tunnel_dest_port}'
#        elif 'L' in tunnel_mode or :
        cmd = f'''set -e; sshpass -p "{PASS}" ssh {SSH_ARGS} -vvvv -{tunnel_mode} {tconf} {USER}@{IP} \
          || {{ echo FAIL tunnel && exit 1; }} '''
    else:
        cmd =  f'''set -e; sshpass -p "{PASS}" ssh {SSH_ARGS} -vvvv  {USER}@{IP}  || echo FAIL;'''

    if mount:
        mount_local_dir =f'/data/{ALIAS}'
        cmd = f'''
        set +e;
        sudo umount -fl {mount_local_dir};
        set -e;
        sshfs -o nonempty,reconnect {USER}@{IP}:{mount_remote_dir} {mount_local_dir} \
         -o ssh_command="$(echo sshpass -p {PASS} ssh {SSH_ARGS})";
        ''' + cmd

    if verbose is True or dry is True:
        print(f'[CMD]\n  {cmd}')

    if dry is True:
        pass
    else:
        _system(cmd)


    '''
    SSH_ARGS="-p $SSH_PORT"
    mkdir -p /data/$ALIAS; umount -fl /data/$ALIAS || echo [unmount]FAIL;
    sshfs -o nonempty,reconnect ${USER}@${IP}:/home/td /data/$ALIAS \
     -o ssh_command="$(echo sshpass -p $PASS ssh ${SSH_ARGS})"

    #if [[ $* == *--tunnel* ]]
    if [[ $TARGET == tunnel ]]
    then
      sshpass -p "$PASS" ssh $SSH_ARGS -vvvv -${FPORTF} $FPORT:localhost:$FPORT ${USER}@${IP}  || { echo FAIL tunnel && exit 1; }
    #sshpass -p "$PASS" ssh $SSH_ARGS -vvvv -NL 8384:localhost:8384 ${USER}@${IP}  || { echo FAIL tunnel && exit 1; }
    #sshpass -p "$PASS" ssh $SSH_ARGS -vvvv -NR 1090:localhost:1090 ${USER}@${IP}  || { echo FAIL tunnel && exit 1; }
    fi
    ‘’‘

    ’‘’
    if [[ $* == *--poweron* ]]
    then
    curl 'https://www.autodl.com/api/v1/instance/power_on' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Authorization: eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjg1NjYsInV1aWQiOiI2NTQxZjdkMC1kNDZjLTRlNjMtYWZjNC0yNmE0NjRjYzE4ZmQiLCJpc19hZG1pbiI6ZmFsc2UsImlzX3N1cGVyX2FkbWluIjpmYWxzZSwic3ViX25hbWUiOiIifQ.PpbCCOyjXkYBQhiL6UU6FBniBmzgPhI1LPMKlgCHzEgEyIpa--8XEGVMnotGSXGPtyi_3Cc3U0pb-zb92cMMCg' -H 'AppVersion: v3.3.0' -H 'Content-Type: application/json;charset=utf-8' -H 'Origin: https://www.autodl.com' -H 'Connection: keep-alive' -H 'Referer: https://www.autodl.com/console/instance/list' -H 'Cookie: _ga_NDC1CJB7XZ=GS1.1.1658833036.45.1.1658833112.0; _ga=GA1.1.423323891.1654328056; Hm_lvt_e24036f31c6b8d171ce550a059a6f6fd=1658035741; Hm_lpvt_e24036f31c6b8d171ce550a059a6f6fd=1658833060' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers' --data-raw '{"instance_uuid":"ee5311983c-4458e12b"}'
    fi

    #exit 0
    #sshpass -p "2pX3kHG193AvyoV2hC" ssh root@$IP || echo FAIL
    sshpass -p "$PASS" ssh $SSH_ARGS -vvvv  ${USER}@${IP}  || echo FAIL
    '''

if __name__=='__main__':
    import sys
    if '--test' in sys.argv:
        main(argv='--ALIAS gcat --PASS somepass --USER ubuntu --SSH_PORT 22 --HOST www.example.com'.split())
        # main(argv='--ALIAS gcat --PASS 123456ok --USER td --SSH_PORT 22 --HOST 192.168.50.132'.split())
    else:
        main()
