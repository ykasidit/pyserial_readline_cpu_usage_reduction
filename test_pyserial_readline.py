import serial
import argparse
import io


def test():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dev',
                        help="serial device path like /dev/ttyACM0",
                        required=True
    )

    parser.add_argument('--baud',
                        help="serial device path like /dev/ttyACM0",
                        default=115200,
                        required=False
    )

    parser.add_argument('--readlen',
                        default=256,
                        required=False
    )

    parser.add_argument('--eval_pyserial_post_setup_code',
                        help="put your custom code here",
                        default=None,
                        required=False
    )

    parser.add_argument('--eval_read_code',
                        help="put your custom read code here",
                        default="readline(256)",
                        required=False
    )

    parser.add_argument('--timeout_secs',
                        default=3,
                        required=False
    )
    
    args = vars(parser.parse_args())

    evalstr = "serial_obj."+args['eval_read_code']
    print 'read code:', evalstr
            
    serial_obj = serial.Serial(args['dev'],timeout=eval(args['timeout_secs']), baudrate=args['baud'])

    if args['eval_pyserial_post_setup_code']:
        print 'set serial_obj to eval of code:', args['eval_pyserial_post_setup_code']
        serial_obj = eval(args['eval_pyserial_post_setup_code'])
    
    with serial_obj:
        while True:
            rbuf = eval(evalstr)
            print 'read string:', rbuf

if __name__ == "__main__":
    test()

