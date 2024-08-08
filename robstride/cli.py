import argparse
import sys

import can

from .client import Client, param_ids_by_name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', type=str, help='The CAN interface to use')
    parser.add_argument('--channel', type=str, help='The channel  for the CAN interface to use')

    subparsers = parser.add_subparsers(dest='command')

    parser_enable = subparsers.add_parser('enable')
    parser_enable.add_argument('motor_id', type=int, help='The ID of the motor to enable')

    parser_disable = subparsers.add_parser('disable')
    parser_disable.add_argument('motor_id', type=int, help='The ID of the motor to disable')

    parser_update_id = subparsers.add_parser('update_id')
    parser_update_id.add_argument('motor_id', type=int, help='The ID of the motor to update')
    parser_update_id.add_argument('new_motor_id', type=int, help='The new ID of the motor')

    parser_zero_pos = subparsers.add_parser('zero_pos')
    parser_zero_pos.add_argument('motor_id', type=int, help='The ID of the motor to zero')
    
    parser_use_control_mode = subparsers.add_parser('use_control_mode')
    parser_use_control_mode.add_argument('motor_id', type=int)
    parser_use_control_mode.add_argument('torque', type=float)
    parser_use_control_mode.add_argument('velocity', type=float)
    parser_use_control_mode.add_argument('position', type=float)
    parser_use_control_mode.add_argument('kp', type=float)
    parser_use_control_mode.add_argument('kd', type=float)
    
    parser_read = subparsers.add_parser('read')
    parser_read.add_argument('motor_id', type=int)
    parser_read.add_argument('param_name', type=str)

    parser_write = subparsers.add_parser('write')
    parser_write.add_argument('motor_id', type=int)
    parser_write.add_argument('param_name', type=str)
    parser_write.add_argument('param_value', type=float)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    run(args)

def run(args):
    with can.interface.Bus(interface=args.interface, channel=args.channel) as bus:
        client = Client(bus)
        if args.command == 'enable':
            client.enable(args.motor_id)
        elif args.command == 'disable':
            client.disable(args.motor_id)
        elif args.command == 'update_id':
            client.update_id(args.motor_id, args.new_motor_id)
        elif args.command == 'zero_pos':
            client.zero_pos(args.motor_id)
        elif args.command == 'use_control_mode':
            client.use_control_mode(args.motor_id, args.torque, args.velocity, args.position, args.kp, args.kd)
        elif args.command == 'read':
            param_id = param_ids_by_name[args.param_name]
            value = client.read_param(args.motor_id, param_id)
            print(f'value: {value}')
        elif args.command == 'write':
            param_id = param_ids_by_name[args.param_name]
            client.write_param(args.motor_id, param_id, args.param_value)

if __name__ == '__main__':
    main()