const int TRIGGER_PIN = 9;
const int ECHO_PIN = 8;

const int LED_VERDE = 5;
const int LED_ROJO = 4;

// Variables
long duracion;
float distancia_cm;

unsigned long ultimoEnvio = 0;
const unsigned long intervaloEnvio = 2000; 

void setup() {
  Serial.begin(9600);

  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);

  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, HIGH); /
}

void loop() {
  distancia_cm = medirDistancia();

  if (distancia_cm > 0 && distancia_cm <= 100) {
   
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_ROJO, LOW);
  } else {
    
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_ROJO, HIGH);
  }


  if (millis() - ultimoEnvio > intervaloEnvio) {
    ultimoEnvio = millis();

    if (distancia_cm > 0 && distancia_cm <= 100) {
      Serial.print("PEATON:");
      Serial.println((int)distancia_cm);
    }
  }

  delay(100);
}

float medirDistancia() {
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  duracion = pulseIn(ECHO_PIN, HIGH, 30000); 
  if (duracion == 0) return -1; 

  return duracion * 0.0343 / 2;
}