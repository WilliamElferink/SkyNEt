# This file contains various functions to use with the switch network
import serial
import numpy as np
import time

def init_serial(comport = 'COM3'):
    '''
    This function initializes a serial object that is used to 
    communicate with the Arduino
    '''
    ser = serial.Serial(port=comport, baudrate=9600, bytesize=8, 
                        parity='N', stopbits=1, write_timeout = 1, 
                        dsrdtr = True)
    return ser

def matrix_to_bytes(matrix):
    '''
    This function converts an 8x8 binary matrix into the proper serial
    signal of 8 bytes that can be sent over the serial port to the 
    Arduino.

    The rows of matrix corresponds to the switching configuration
    of Connectors C1-C8.
    The columns correspond to the devices.
    '''
    # flip in both directions such that c8 recieves first and device numbering is the same as on PCB
    matrix = np.flipud(np.fliplr(matrix))
    
    #send_string = '<'  # Start flag
    send_string = ''

    # Loop over each row of matrix
    for ii, row in enumerate(matrix):
        row_number = 0
        for jj,element in enumerate(row): 
            row_number += 2**jj * element
        send_string += str(row_number)
        if(ii < 7):
            send_string += ','  # Separator character

    #send_string += '>'  # End flag

    return send_string.encode()
            
def switch(ser, matrix):
    '''
    This is the main function that applies the switching configuration
    in matrix to the serial port ser.

    Input arguments
    ---------------
    ser; serial object, to be initialized with init_serial
    matrix; (8, 8) np.array, first row defines the switching 
            configuration of C1.
    '''
    send_string = matrix_to_bytes(matrix)

    ser.write('<'.encode())
    time.sleep(0.2)

    ser.write(send_string)
    time.sleep(0.2)

    ser.write('>'.encode())
    time.sleep(0.2)

def connect_single_device(ser, device_number):
    '''
    This function connects the device number device_number (1-8 on PCB)
    to the BNC connectors
    '''
    assert (device_number>0 and device_number<9), "Device number must be in range (1-8)"
    matrix = np.zeros((8, 8))
    matrix[:, device_number-1] = 1
    switch(ser, matrix)

def close(ser):
    ser.close()