#define CHECK_BIT(var, pos) (((var)>>(pos)) & 1)
#define TOGGLE_BIT(var, pos) (var ^= (1L << pos))

#define BOUNCE_DELAY 500

// Rows are inputs
int row_pins[] = {34, 35};
// columns are outputs
int column_pins[] = {2, 3};
int number_of_rows = 2;
int number_of_columns = 2;

String str;

void setup() {
        // We will scan over rows, so set these as outputs
        for(int i = 0; i < number_of_rows; i++){
                pinMode(row_pins[i], OUTPUT);
        }

        // We will read across columns, so set these as inputs
        for(int i = 0; i < number_of_columns; i++) {
                pinMode(column_pins[i], INPUT);
        }

        Serial.begin(9600);
}

void loop() {
        // 64 zeros to represent the states of the pieces
        static uint64_t lastPieceState = LOW;
        // Loop over rows
        for(int i = 0; i < number_of_rows; i++){
                // First, set each row high, one at a time
                digitalWrite(row_pins[i], HIGH);

                // Then, for each column...
                for(int j = 0; j < number_of_columns; j++){
                // Calculate which square we're on, between 0 and 63
                        int current_square = i * number_of_columns + j;
                        // Read the pin corresponding to column j
                        int pinState = digitalRead(column_pins[j]);
                        // If the state has changed since the last time we read...
                        if(pinState != CHECK_BIT(lastPieceState, current_square)) {
                                // Update the stored state to represent this...
                                TOGGLE_BIT(lastPieceState, current_square);
                                if(pinState == HIGH){
                                        // ...and print the square number, and 'down' if it's high
                                        Serial.println(str + current_square + " " + "down");
                                } else if(pinState == LOW){
                                        // ...and print the square number, and 'up' if it's low
                                        Serial.println(str + current_square + " " + "up");
                                }
                                // Wait a little while, to prevent reading switch bouncing
                                delay(BOUNCE_DELAY);
                        }
                }
                // Then set the corresponding row low again
                digitalWrite(row_pins[i], LOW);
        }
}
