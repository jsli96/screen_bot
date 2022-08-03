# screen_bot
This script service Scrren Robot project.
PI Zero W GPIO Pin-out diagram:
https://cdn.sparkfun.com/assets/learn_tutorials/6/7/6/PiZero_1.pdf

The script has four parts:
  1. cloud server code
  2. raspberry pi code
  3. image match code
  4. web UI


Pi zero GPIO Pinout:

    MOTOR_A_PWM = 'GPIO12'     # PWM input for extension motor
    MOTOR_A_PHASE = 'GPIO5'    # Phase input for extension motor
    MOTOR_B_PWM = 'GPIO13'     # PWM input for rotation motor
    MOTOR_B_PHASE = 'GPIO6'    # Phase input for rotation motor
    ROTATION_C1 = 'GPIO21'     # Motor encoder C1
    ROTATION_C2 = 'GPIO20'     # Motor encoder C2
    ROTATION_VCC = 'GPIO16'    # Encoder power line
    IR_1 = 'GPIO23'            # IR Sensor 1
    IR_2 = 'GPIO24'            # IR Sensor 2
    IR_VCC = 'GPIO26'          # IR Sensor Power line