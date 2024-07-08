import piir
import argparse

#location = "/home/pi/git/piFan"
location = "/home/ub/Documents/github/piFan"

def send_action(action):
    remote.send(action)
    print(f"Sending action: {action}")

valid_actions = {
    "light_on": "light_on",
    "light_off": "light_off",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "fan_off": "fan_off",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h"
}

action_descriptions = {
    "light_on": "Light_On turns on the light",
    "light_off": "Light_Off turns off the light",
    "low": "Low sets the fan to low speed",
    "medium": "Medium sets the fan to medium speed",
    "high": "High sets the fan to high speed",
    "fan_off": "Fan_Off turns off the fan",
    "1h": "1h sets the timer to 1 hour",
    "2h": "2h sets the timer to 2 hours",
    "4h": "4h sets the timer to 4 hours"
}

help_message = "Action to send:\n"
for action, description in action_descriptions.items():
    help_message += f"  {action}: {description}\n"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send actions to fan over IR", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-action", type=str, required=True, help=help_message)
    args = parser.parse_args()

    gpio_pin = 27
    ir_file = f"{location}/scripts/record.json"
    remote = piir.Remote(ir_file, gpio_pin)
    action = args.action.lower()

    if action.lower() in valid_actions:
        send_action(valid_actions[action])
    else:
        print("Error: Invalid action")