/**
 *	@file		IMUino.pde
 *	@version	0.10beta
 *
 *	@author		Francesco Cruciani, Francesco Vitullo
 *	@note		ArduIMU - Arduino binary serial communication
 *				15/02/2011 - www.codesigns.it
 */

// pin for serial input in arduino
#define RX 0
// serial rate for arduIMU
#define IMU_SERIAL_RATE 38400
// message tag
#define IMU_TAG "DIYd"
// number of messages send
#define IMU_VALUES 3

int counter=0;

// union structure for serial received binary data
typedef union{
	int16_t word;
	byte	valByte[2];
} IMUpacket;

// intialization of the structures for each passed value
IMUpacket serialPackets[IMU_VALUES];
// first tag in message
char imuTag[] = IMU_TAG;
// first tag in message buffer
char IMUtagBuffer[sizeof(imuTag)];
// check for new data
boolean newData = false;
// vars for checksum
byte msg_checksum_a;
byte msg_checksum_b;

// waits for n bytes to receive
void wait_for_bytes(byte number){
	while(Serial.available() < number);
}
// sums all the values and confront the result with the checksum passed
boolean checksum_is_true(){
	byte current_msg_checksum_a = 0;
	byte current_msg_checksum_b = 0;
	for(uint8_t i=0; i<IMU_VALUES; i++){
		current_msg_checksum_a += serialPackets[i].valByte[0];
		current_msg_checksum_b += current_msg_checksum_a;
                current_msg_checksum_a += serialPackets[i].valByte[1];
		current_msg_checksum_b += current_msg_checksum_a;
	}

	return (current_msg_checksum_a == msg_checksum_a && current_msg_checksum_b == msg_checksum_b);
}

void setup(){
	Serial.begin(IMU_SERIAL_RATE);
	pinMode(RX, INPUT);
}

void loop(){
	if(Serial.available()>0){
                counter++;
		// check if the byte is the start of new messange
		wait_for_bytes(1);
		IMUtagBuffer[0] = Serial.read(); //  D
		if(IMUtagBuffer[0]==imuTag[0]){
			wait_for_bytes(3);
			IMUtagBuffer[1] = Serial.read(); // I
			IMUtagBuffer[2] = Serial.read(); // Y
			IMUtagBuffer[3] = Serial.read(); // d

			if(IMUtagBuffer[1]==imuTag[1] && IMUtagBuffer[2]==imuTag[2] && IMUtagBuffer[3]==imuTag[3]){
				// new messange
				newData = true;
				// receive all values and put it in the packet structure
				wait_for_bytes((IMU_VALUES*2)+2);

				serialPackets[0].valByte[0] = Serial.read();
				serialPackets[0].valByte[1] = Serial.read(); // roll

				serialPackets[1].valByte[0] = Serial.read();
				serialPackets[1].valByte[1] = Serial.read(); // pitch

				serialPackets[2].valByte[0] = Serial.read();
				serialPackets[2].valByte[1] = Serial.read(); // yaw

				msg_checksum_a = Serial.read();
				msg_checksum_b = Serial.read(); // checksum
			} else newData = false;
		}

		// checksum for message
		if(newData && checksum_is_true()){
                        /*
			// do stuff with received data values
                        Serial.print("roll: ");
			Serial.println(serialPackets[0].word/100);
                        Serial.print("pitch: ");
                        Serial.println(serialPackets[1].word/100);
			Serial.print("yaw: ");
                        Serial.println(serialPackets[2].word/100);
                        */
                        Serial.println(counter);
		} else{
			msg_checksum_a = 0;
			msg_checksum_b = 0;
		}
	}
}

