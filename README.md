# HDR Light Field Capture
Code for capturing Hight Dynamic Range light fields

[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]

One to two paragraph statement about your product and what it does.

![](header.png)

## Hardware
### Motor Control
Arduino code:

```int stepPin = 5;

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
```

## Installation

OS X & Linux:

```sh
npm install my-crazy-module --save
```

Windows:

```sh
edit autoexec.bat
```

## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Release History

* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

## Meta

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki