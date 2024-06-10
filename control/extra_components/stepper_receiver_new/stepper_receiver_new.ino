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
    Serial.begin(115200);
    // Set up pin modes for motor control

    pinMode(STEP_Base, OUTPUT);
    pinMode(DIR_Base, OUTPUT);

    pinMode(STEP_Extruder, OUTPUT);
    pinMode(DIR_Base, OUTPUT);
}

void loop() {
    read_input();  
}

//read input that is called every loop iteration
void read_input(){
  
  //read icoming text and transform it
  char buffer[32]; // Buffer to hold incoming data
  Serial.setTimeout(8);
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

  //command in the form of : 'cb[position base]s[speedbase]e[extruderposition]t[extruderspeed]i[index]
  //Serial.println("\nAckknowleged: combined turning initiated: " + command);

  int bIndex = command.indexOf('b');
  int sIndex = command.indexOf('s');
  int eIndex = command.indexOf('e');
  int tIndex = command.indexOf('t');
  int iIndex = command.indexOf('i');

  // Extract the position and speed from the command String
  String basepositionString = command.substring(bIndex + 1, sIndex);
  String basespeedString = command.substring(sIndex + 1,eIndex);
  String extruderpositionString = command.substring(eIndex + 1, tIndex);
  String extruderspeedString = command.substring(tIndex+1, iIndex);
  String indexString = command.substring(iIndex + 1);

  // Convert the position and speed to integers
  int extruderspeed = extruderspeedString.toInt();
  int extruder_position = extruderpositionString.toInt();
  int base_position = basepositionString.toInt();
  int basespeed = basespeedString.toInt();   
  int index = indexString.toInt();

  //calc steps and speed

  int base_stepgoal = setStepsNumber(base_position, previous_base_position);
  int extruder_stepgoal = setStepsNumber(extruder_position, previous_extruder_position);
  float base_halfPulseDuration = setRotationSpeed(basespeed);
  float extruder_halfPulseDuration = setRotationSpeed(extruderspeed);

  previous_base_position = base_position;
  previous_extruder_position = extruder_position;
  
  //actually move the motors
  move_combined(base_stepgoal, extruder_stepgoal, base_halfPulseDuration, extruder_halfPulseDuration);
    
  
  Serial.println("-done i" + String(index)); 
  //Serial.println("done i" + String(index)); 


}

void move_combined(int steps_base, int steps_extruder, float halfPulseDuration_base, float halfPulseDuration_extruder){


  if(steps_base > 0){
    digitalWrite(DIR_Base, LOW); 
  }else{
    digitalWrite(DIR_Base, HIGH);
  }
  
  //does not work because of the motor for some reason - change polarity with the cable if necessary
  if(steps_extruder > 0){
    digitalWrite(DIR_Extruder, HIGH);
  }else{
   digitalWrite(DIR_Extruder, LOW);}
   

  extruder_high = false;
  base_high = false;
  
  double previous_extruder_steptime = micros();
  double previous_base_steptime = micros();
  int steps_done_base = 0;
  int steps_done_extruder = 0;


  
    while(steps_done_base < abs(steps_base) || steps_done_extruder < abs(steps_extruder)){
        
        //switch base
        if((micros() - previous_base_steptime) > halfPulseDuration_base && steps_done_base < abs(steps_base)){
                switch_base();
                previous_base_steptime = micros();
                steps_done_base++;
              }


        if((micros() - previous_extruder_steptime) > halfPulseDuration_extruder && steps_done_extruder < abs(steps_extruder)){
                switch_extruder();
                previous_extruder_steptime = micros();
                steps_done_extruder++;
              }
          
    }  

      digitalWrite(STEP_Base, LOW);
      digitalWrite(DIR_Base, LOW);
      last_time = micros();
      delay(100);
      Serial.println("done");

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
  else if(command.startsWith("c")) // command "cb[position base]s[speedbase]e[extruderposition]t[extruderspeed]i[index]"
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








