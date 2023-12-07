//Pressure Sensor Initializations
const int pressureSensorPin = A0; // Analog pin for the pressure sensor
const int rgbLedPinRed_p = 9;      // Digital pin for the red component of the RGB LED
const int rgbLedPinGreen_p = 11;    // Digital pin for the green component of the RGB LED


//Ultrasound Sensor Initializations
const int trigPin = 2;  // Digital pin for the ultrasonic sensor trigger
const int echoPin = 3;  // Digital pin for the ultrasonic sensor echo
const int rgbLedPinRed_u = 5;    // Digital pin for the red component of the RGB LED
const int rgbLedPinGreen_u = 6;  // Digital pin for the green component of the RGB LED

//Thresholds
const int pressureThreshold = 500; // Adjust this value based on your sensor and requirements
const int redThreshold = 20;  // Adjust this value based on your distance requirement (in centimeters)


void setup() {
  //Pressure Sensor Setup
  pinMode(rgbLedPinRed_p, OUTPUT);
  pinMode(rgbLedPinGreen_p, OUTPUT);
  Serial.begin(9600);
  analogWrite(10, 192);

  //Ultrasound Sensor Setup
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(rgbLedPinRed_u, OUTPUT);
  pinMode(rgbLedPinGreen_u, OUTPUT);
  digitalWrite(1, HIGH);
  digitalWrite(4, LOW);
}

void loop() {
  int pressureValue = analogRead(pressureSensorPin);

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;


  // Print the pressure value to the Serial Monitor for debugging
  Serial.print("Pressure Value: ");
  Serial.print(pressureValue);
  Serial.print("\t");
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");


  if (pressureValue > pressureThreshold) {
    digitalWrite(rgbLedPinRed_p, HIGH);   // Turn on the red component
    digitalWrite(rgbLedPinGreen_p, LOW);  // Turn off the green component
    Serial.println("Pressure detected! Red LED ON");
  } else {
    digitalWrite(rgbLedPinRed_p, LOW);    // Turn off the red component
    digitalWrite(rgbLedPinGreen_p, HIGH);  // Turn on the green component
  }

  if (distance <= redThreshold) {
    digitalWrite(rgbLedPinRed_u, HIGH);    // Turn on the red component
    digitalWrite(rgbLedPinGreen_u, LOW);   // Turn off the green component
    Serial.println("Danger! Red LED ON");
  } else {
    digitalWrite(rgbLedPinRed_u, LOW);     // Turn off the red component
    digitalWrite(rgbLedPinGreen_u, HIGH);  // Turn on the green component
    Serial.println("Safe. Green LED ON");
  }

  delay(200); // Adjust the delay as needed
}
