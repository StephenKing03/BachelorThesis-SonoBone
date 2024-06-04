///////////////////////////////////////////////
//     SonoBone ROBOTIC ARM Arduino Code     //
//                                           //
//                                           //
//              Stephan Koenig               //
//      using code from Dimitar Boev         //
//                                           //
//                ETH ZURICH                 //
//                                           //
//     ACOUSTIC ROBOTICS SYSTEMS LABORATORY  //
///////////////////////////////////////////////

String command = "";
float previous_base_position = 0;
float previous_extruder_half_duration = 0;
float previous_extruder_position;
bool continue_extruder = false;
float previous_switchtime = micros();
bool extruder_high = false;
bool base_high = false;
float last_time = micros();


// STEP_PIN , DIR_PIN for small CNC Shield
// X - 2,5 ; Y - 3,6 ; Z - 4,7 ; R - 12,130

// Motor pins
#define STEP_Base 2
#define DIR_Base  5

#define STEP_Extruder 3
#define DIR_Extruder 6


void setup() {
    Serial.begin(2000000);
    // Set up pin modes for motor control

    pinMode(STEP_Base, OUTPUT);
    pinMode(DIR_Base, OUTPUT);

    pinMode(STEP_Extruder, OUTPUT);
    pinMode(DIR_Base, OUTPUT);
}

void loop() {
    read_input();
    handle_leftover_extruder_rotation();
}

void handle_leftover_extruder_rotation(){

  if(continue_extruder && micros()  - previous_switchtime > previous_extruder_half_duration){
    switch_extruder();
  }

  if(continue_extruder == false || micros() - last_time > 100000000 ){
    digitalWrite(STEP_Extruder, LOW);
    extruder_high = false;
    continue_extruder = false;
    //Serial.println("timed out");
  }

}

//read input that is called every loop iteration
void read_input(){
  
  //read icoming text and transform it
  char buffer[32]; // Buffer to hold incoming data
  Serial.setTimeout(2);
  int length = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
  buffer[length] = '\0'; // Null-terminate the String
  String input = String(buffer);
  
  if (input != ""){
      process_data(input);
  }

  return;
}

long setStepsNumber(float position, float previous_position) {

    float distanceInDeg = position - previous_position;
    float degPerStep = 1.8/16; // Adjust this value based on your stepper motor specifications
    int steps = distanceInDeg / degPerStep;
    
    //Serial.print(" steps to execute: ");
    //Serial.println(steps);
    return steps;
}

float setRotationSpeed(float speed) {
    
    int STEPS_PER_REVOLUTION = 200;
    int MICROSTEPPING_FACT = 16;
    return 1000000L * 360L / 2L / STEPS_PER_REVOLUTION / MICROSTEPPING_FACT / speed;
}


//function to turn the base to a certain position
bool turn_base(String command){

  Serial.println("\nAckknowleged: base turning to position");

  int pIndex = command.indexOf('b');
  int sIndex = command.indexOf('s');
  int iIndex = command.indexOf('i');

  // Extract the position and speed from the command String
  String positionString = command.substring(pIndex + 1, sIndex);
  String speedString = command.substring(sIndex + 1,iIndex);
  String indexString = command.substring(iIndex + 1);

  // Convert the position and speed to integers
  int position = positionString.toInt();
  int speed = speedString.toInt();   
  int index = indexString.toInt();


  //calc steps and speed
  int stepgoal = setStepsNumber(position, previous_base_position);
  float halfPulseDuration = setRotationSpeed(speed);
  previous_base_position = position;
  
  
  //actually move the motors
  move_base_solo(stepgoal, halfPulseDuration);
  Serial.println("-done i" + String(index));
}
void turn_extruder(String command){

  Serial.println("\nAckknowleged: extruder turning to position");

  int pIndex = command.indexOf('e');
  int sIndex = command.indexOf('s');
  int iIndex = command.indexOf('i');

  // Extract the position and speed from the command String
  String positionString = command.substring(pIndex + 1, sIndex);
  String speedString = command.substring(sIndex + 1,iIndex);
  String indexString = command.substring(iIndex + 1);

  // Convert the position and speed to integers
  int position = positionString.toInt();
  int speed = speedString.toInt();   
  int index = indexString.toInt();


  //calc steps and speed
  int stepgoal = setStepsNumber(position, previous_extruder_position);
  float halfPulseDuration = setRotationSpeed(speed);
  previous_extruder_position = position;
  
  
  //actually move the motors
  move_extruder_solo(stepgoal, halfPulseDuration);
  Serial.println("-done i" + String(index));
  
}

void move_extruder_solo(int steps, float halfPulseDuration) {

    //set direction
    if(steps > 0){
      digitalWrite(DIR_Extruder, LOW); 
    }else{
      digitalWrite(DIR_Extruder, HIGH);
    }

    for (int i = 0; i < abs(steps); i++) {
        digitalWrite(STEP_Extruder, HIGH);
        delayMicroseconds(halfPulseDuration);
        digitalWrite(STEP_Extruder, LOW);
        delayMicroseconds(halfPulseDuration);
    }

    digitalWrite(STEP_Extruder, LOW);
    digitalWrite(DIR_Extruder, LOW);
    continue_extruder = false;
}



void move_base_solo(int steps, float halfPulseDuration) {

    //set direction
    if(steps > 0){
      digitalWrite(DIR_Base, LOW); 
    }else{
      digitalWrite(DIR_Base, HIGH);
    }

    for (int i = 0; i < abs(steps); i++) {
        digitalWrite(STEP_Base, HIGH);
        delayMicroseconds(halfPulseDuration);
        digitalWrite(STEP_Base, LOW);
        delayMicroseconds(halfPulseDuration);
    }

    digitalWrite(STEP_Base, LOW);
    digitalWrite(DIR_Base, LOW);
}

void init_motors(){

  int speed = 200;
  int position = 90;

  int stepgoal = setStepsNumber(position, previous_base_position);
  float halfPulseDuration = setRotationSpeed(speed);


  move_base_solo(stepgoal, halfPulseDuration);
  move_base_solo(-stepgoal, halfPulseDuration);

  
  Serial.println("initialized");
}
void combined_turning(String command){

  Serial.println("\nAckknowleged: combined turning initiated: " + command);

  int cIndex = command.indexOf('c');
  int bIndex = command.indexOf('b');
  int sIndex = command.indexOf('s');
  int iIndex = command.indexOf('i');

  // Extract the position and speed from the command String
  String extruderString = command.substring(cIndex + 1, bIndex);
  String positionString = command.substring(bIndex + 1, sIndex);
  String speedString = command.substring(sIndex + 1,iIndex);
  String indexString = command.substring(iIndex + 1);

  // Convert the position and speed to integers
  int extruder = extruderString.toInt();
  int position = positionString.toInt();
  int speed = speedString.toInt();   
  int index = indexString.toInt();

  //calc steps and speed
  int extruder_halfPulse = setRotationSpeed(abs(extruder));
  int stepgoal = setStepsNumber(position, previous_base_position);
  float halfPulseDuration = setRotationSpeed(speed);
  previous_base_position = position;
  
  
  //actually move the motors
  move_combined(stepgoal, extruder, halfPulseDuration, extruder_halfPulse);
    
  
  Serial.println("done i" + String(index)); 


}

void move_combined(int steps_base, int direction_extruder, float halfPulseDuration_base, float halfPulseDuration_extruder){

  continue_extruder = true;
  //Serial.print("Base duration: " + String(halfPulseDuration_base) + "; Extruder:" + String(halfPulseDuration_extruder)+ "Extruder Direction: " + String(direction_extruder));
  //set direction
  if(steps_base > 0){
    digitalWrite(DIR_Base, LOW); 
  }else{
    digitalWrite(DIR_Base, HIGH);
  }
  
  if(direction_extruder > 0){
    digitalWrite(DIR_Extruder, HIGH);
  }else{
   digitalWrite(DIR_Extruder, LOW);}
   

  extruder_high = false;
  base_high = false;
  
  previous_switchtime = micros();
  double previous_base_steptime = micros();
  int steps_done = 0;
  
    while(steps_done < abs(steps_base)){
        
        if((micros() - previous_base_steptime) > halfPulseDuration_base){
                switch_base();
                previous_base_steptime = micros();
                steps_done++;
              }


        if((micros() - previous_switchtime) > halfPulseDuration_extruder){
                switch_extruder();
                previous_switchtime = micros();
              }
          
    }  

      digitalWrite(STEP_Base, LOW);
      digitalWrite(DIR_Base, LOW);
      last_time = micros();

}

void reset_position_to(String command){

 int rIndex = command.indexOf('r');
 String rString = command.substring(rIndex + 1); 
 int position = rString.toInt();

 previous_base_position = position;

}

void switch_extruder(){

  if(extruder_high == true){
    digitalWrite(STEP_Extruder, LOW);
    extruder_high = false;
  }else{
    digitalWrite(STEP_Extruder, HIGH);
    extruder_high = true;
  }
}

void switch_base(){

  if(base_high == true){
    digitalWrite(STEP_Base, LOW);
    base_high = false;
  }else{
    digitalWrite(STEP_Base, HIGH);
    base_high = true;
  }
}

void process_data(String command){

  if(command.startsWith("init")) // command "init"
    {init_motors();}
  else if(command.startsWith("b")) // command "b[abs_position]s[turning_speed]i[confirmation_index]"
    { turn_base(command);}
  else if(command.startsWith("c")) // command "c[speed_extruder]b[abs_position]s[base_turning_speed]i[confirmation_index]"
    {combined_turning(command);}
  else if (command.startsWith("exstop")) //command "exstop"
    { Serial.println("extruder stopped");
      continue_extruder = false;}
  else if (command.startsWith("e")){ // command "e[steps extruder]s[speed extruder]"
      turn_extruder(command);}
  else if (command.startsWith("r"))
      {reset_position_to(command); }
  else
    {Serial.println("Invalid Command. Command was: " + String(command));}
}








