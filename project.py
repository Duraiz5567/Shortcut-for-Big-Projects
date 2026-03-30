import datetime
import os
import re


def file_read(car_filename):
    if not os.path.exists(car_filename):
        # Return an empty list if the file doesn't exist
        return []
    with open(car_filename, "r") as myfile:
        return myfile.readlines()


def write_file(car_filename, data):
    if not os.path.exists(car_filename):
        # Return an empty list if the file doesn't exist
        return []    
    with open(car_filename, "w+") as myfile:
        myfile.writelines(data)


def append_to_file(car_filename, line):
    if not os.path.exists(car_filename):
        # Return an empty list if the file doesn't exist
        return []    
    with open(car_filename, "a") as myfile:
        myfile.write(line + "\n")


def calculate_client_age(birthday_date):   
    client_birth_date = datetime.datetime.strptime(birthday_date, "%d/%m/%Y")
    today = datetime.datetime.today()
    client_age = today.year - client_birth_date.year - ((today.month, today.day) < (client_birth_date.month, client_birth_date.day))
    return client_age
#
def main():
    """Main menu and program execution."""
    while True:
        print("\nMenu:")
        print("1. List available cars")
        print("2. Rent a car")
        print("3. Return a car")
        print("4. Count the money")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            """Displays all available cars that are not rented."""
            vehicles = file_read("vehicles.txt")
            rented = [line.split(",")[0] for line in file_read("rentedVehicles.txt")]

            # Using a list comprehension for available cars
            available_cars = [line for line in vehicles if line.split(",")[0] not in rented]
            print("\nAvailable cars for rent:")
            for car in available_cars:
                print(f"# {car.strip()}")

        elif choice == "2":            
            vehicles = file_read("vehicles.txt")
            rented = file_read("rentedVehicles.txt")
            rented_cars = [line.split(",")[0] for line in rented]

            while True:
                registeration_number = input("Enter the registration_number of the car : ").strip()
                if not any(car.startswith(registeration_number) for car in vehicles):
                    print("Your given registeration number is invalid. Please try again.")
                elif registeration_number in rented_cars:
                    print("Your given registeration number is already rented.")
                    return
                else:
                    break

            while True:
                birthday_date = input("Please enter your birthday in the form DD/MM/YYYY: ").strip()
                try:
                    client_age = calculate_client_age(birthday_date)
                    if client_age < 18:
                        print("You are too young to rent a car.")
                        return
                    elif client_age > 80:
                        print("You are too old to rent a car.")
                        return
                    break
                except ValueError:
                    print("Your given date format is invalid. Try again.")

            while True:
                f_name = input("Enter your first name: ").strip()
                l_name = input("Enter your last name: ").strip()
                if f_name.isalpha() and l_name.isalpha() and f_name[0].isupper() and l_name[0].isupper():
                    break
                else:
                    print("First name and Last name must contain only letters and start with a capital letter.")

            while True:
                email = input("Enter your email: ").strip()
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    break
                else:
                    print("Your given email format is invalid. Try again.")

            print(f"\nHello, {f_name} {l_name}")
            print(f"You rented the car registration number {registeration_number}")

            # Append to customers.txt if not already present
            customers = file_read("customers.txt")
            if not any(line.startswith(birthday_date) for line in customers):
                append_to_file("customers.txt", f"{birthday_date},{f_name},{l_name},{email}")

            # Add to rentedVehicles.txt
            rent_start = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            append_to_file("rentedVehicles.txt", f"{registeration_number},{birthday_date},{rent_start}")

        elif choice == "3":
            # Return a rented car
            rented = [line.strip() for line in file_read("rentedVehicles.txt")]  # Strip newlines
            vehicles = file_read("vehicles.txt")

            registeration_number = input("Enter the registration number of the car to return: ").strip()
            rented_entry_of_car = next(
                (line for line in rented if line.split(",")[0] == registeration_number), None
            )

            if not rented_entry_of_car:
                print("Car not found or not rented.")
                return

            # Remove the car entry from the rented list
            rented.remove(rented_entry_of_car.strip())  # Ensure stripping matches

            rented_data = rented_entry_of_car.split(",")
            car_reg, customer_birthday_date, rent_start = rented_data

            rental_start_date = datetime.datetime.strptime(rent_start, "%d/%m/%Y %H:%M")
            rental_end_date = datetime.datetime.now()
            days_rented = (rental_end_date - rental_start_date).days + 1

            daily_rate = next(
                (int(line.split(",")[2]) for line in vehicles if line.startswith(car_reg)), None
            )
            if daily_rate is None:
                print("Car details not found.")
                return

            cost = days_rented * daily_rate
            print(f"The rent lasted {days_rented} days, and the cost is {cost:.2f} euros.")

            # Update rentedVehicles.txt
            write_file("rentedVehicles.txt", [line + "\n" for line in rented])
            # Append transaction to transActions.txt
            append_to_file(
                "transActions.txt",
                f"{car_reg},{customer_birthday_date},{rent_start},{rental_end_date.strftime('%d/%m/%Y %H:%M')},{days_rented},{cost:.2f}",
            )
        elif choice == "4":           
            transactions = file_read("transActions.txt")
            total = sum(float(line.split(",")[-1]) for line in transactions)
            print(f"Company's total earnings: {total:.2f} euros")

        elif choice == "0":
            print("Car management system is goint to exit. Goodbye!")
            break
        else:
            print("your entered is option is invalid. Please try again.")


if __name__ == "__main__":
    main()
