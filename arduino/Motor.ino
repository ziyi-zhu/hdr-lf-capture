int stepPin = 5;
int dirPin = 6;
int enblPin = 7;

int buttonPin = A0;

int STEP_DELAY = 600;
int MAX_STEP = 27000;
int UNIT_STEP = MAX_STEP / 100;

char instruction;
int motorStep;

void(* resetFunc) (void) = 0;

void moveToLocation(int finalStep) {
  if(finalStep < motorStep) {
    digitalWrite(dirPin, LOW);
  }
  else if(finalStep > motorStep) {
    digitalWrite(dirPin, HIGH);
  }

  digitalWrite(enblPin, HIGH);

  while(motorStep != finalStep) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(STEP_DELAY);

    if(digitalRead(dirPin) == 0) {motorStep -= 1;}
    else {motorStep += 1;}
  }

  digitalWrite(enblPin, LOW);
  Serial.println("End");
}

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enblPin, OUTPUT);

  pinMode(buttonPin, INPUT);
  
  digitalWrite(stepPin, LOW);
  digitalWrite(dirPin, LOW);
  digitalWrite(enblPin, HIGH);

  while(digitalRead(buttonPin) == 0) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(STEP_DELAY);
  }

  digitalWrite(enblPin, LOW);

  motorStep = 0;
  
  Serial.begin(9600);
}

void loop() {
  if((motorStep <= 0 && digitalRead(dirPin) == 0)||(motorStep >= MAX_STEP && digitalRead(dirPin) == 1)) {
    digitalWrite(enblPin, LOW);
  }
  
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(STEP_DELAY);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(STEP_DELAY);

  if(digitalRead(enblPin) == 1) {
    if(digitalRead(dirPin) == 0) {motorStep -= 1;}
    else {motorStep += 1;}
  }
   
  if(Serial.available() > 0) {
    instruction = Serial.read();

    if(instruction == '1') {
      digitalWrite(dirPin, HIGH);
      digitalWrite(enblPin, HIGH);
    }
    else if(instruction == '2') {
      digitalWrite(dirPin, LOW);
      digitalWrite(enblPin, HIGH);
    }
    else if(instruction == '0') {
      digitalWrite(enblPin, LOW);
      Serial.println(map(motorStep, 0, MAX_STEP, 0, 100));
    }
    else if(instruction == 'x') {
      int motorSpeed = Serial.readString().toInt();
      STEP_DELAY = map(motorSpeed, 1, 10, 1000, 100);
    }
    else if(instruction == 'm') {
      int finalStep = map(Serial.readString().toInt(), 0, 100, 0, MAX_STEP);
      moveToLocation(finalStep);
    }
    else if(instruction == 'f') {
      moveToLocation(motorStep + UNIT_STEP);
    }
    else if(instruction == 'b') {
      moveToLocation(motorStep - UNIT_STEP);
    }
    else if(instruction == 'r') {
      resetFunc();
    }
  }
}
