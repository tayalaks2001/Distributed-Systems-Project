package main

import (
	"fmt"
	"net"
	"os"
	"time"
)

const TIMEOUT = 5

type client struct {
	net.Conn
}

func menu() (option int) {
	fmt.Println("Menu:")
	fmt.Println("1) Create new account")
	fmt.Println("2) Delete account")
	fmt.Println("3) Deposit money")
	fmt.Println("4) Withdraw money")
	fmt.Println("5) Query Balance")
	fmt.Println("6) Transfer money")
	fmt.Println("7) Monitor changes")
	fmt.Println("8) Exit")
	for {
		fmt.Print("Please enter an option between 1-8 :")
		_, err := fmt.Scanf("%d", &option)
		if err == nil && option >= 1 && option <= 8 {
			break
		}
		fmt.Println("Invalid option, please try again")
	}
	if option == 8 {
		fmt.Println("Exiting..")
		os.Exit(0)
	}
	return
}

func getInt() (val int) {
	for {
		fmt.Print("Please enter an unsigned int:")
		_, err := fmt.Scanf("%d", &val)
		if err == nil {
			break
		}
		fmt.Println("Invalid input, please try again")
	}
	return
}

func getString() (val string) {
	for {
		fmt.Print("Please enter a string:")
		_, err := fmt.Scanf("%s", &val)
		if err == nil {
			break
		}
		fmt.Println("Invalid input, please try again")
	}
	return
}

func getFloat() (val float32) {
	for {
		fmt.Print("Please enter a float:")
		_, err := fmt.Scanf("%f", &val)
		if err == nil {
			break
		}
		fmt.Println("Invalid input, please try again")
	}
	return
}

func createMessage(option int) (msg interface{}) {

	switch option {
	case 1:
		{
			fmt.Println("Creating new account...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Password")
			password := getString()
			fmt.Println("Enter Initial Balance")
			balance := getFloat()
			fmt.Println("Enter Currency Type")
			currencyType := getInt()
			// msg = CreateNewAccountMessage{} blah blah
		}
	case 2:
		{
			fmt.Println("Closing account...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter Password")
			password := getString()
		}
	case 3:
		{
			fmt.Println("Depositing money...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter Password")
			password := getString()
			fmt.Println("Enter Currency Type")
			currencyType := getInt()
			fmt.Println("Enter Ammount")
			ammount := getFloat()
		}
	case 4:
		{
			fmt.Println("Withdrawing money...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter Password")
			password := getString()
			fmt.Println("Enter Currency Type")
			currencyType := getInt()
			fmt.Println("Enter Ammount")
			ammount := getFloat()
		}
	case 5:
		{
			fmt.Println("Querying balance...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter Password")
			password := getString()
		}
	case 6:
		{
			fmt.Println("Transfering money...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter your Account Number")
			accNum := getInt()
			fmt.Println("Enter Password")
			password := getString()
			fmt.Println("Enter Currency Type")
			currencyType := getInt()
			fmt.Println("Enter Ammount")
			ammount := getFloat()
			fmt.Println("Enter Recepient Account Number")
			rcvAccNum := getInt()
		}

	case 7:
		{
			fmt.Println("Requesting to monitor...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter Password")
			password := getString()
			fmt.Println("Enter Duration in minutes")
			duration := getInt()
		}
	}
	return msg
}

func ClientLoop(address string) {
	var err error
	c := &client{}

	c.Conn, err = net.Dial("udp", address)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(-1)
	}

	for {

		var data []byte
		// send some stuff
		// menu ...
		option := menu()
		msg := createMessage(option)
		// data = marshalled blah blah

		reply, err := c.sendAndRecvMsg(data)
		if err == nil {
			fmt.Println(string(reply))
			if option == 7 {
				// check if response recvd was correct
				// c.monitor(msg.duration)
			}
		}
	}
}

func (c *client) monitor(duration int) {
	endTime := time.Now().Add(time.Minute * time.Duration(duration))
	replyBuf := make([]byte, 1024)
	defer c.Conn.SetDeadline(time.Time{})
	defer fmt.Println("Monitor duration ended")

	for endTime.After(time.Now()) {
		c.SetReadDeadline(endTime)
		n, err := c.Conn.Read(replyBuf)
		if err != nil {
			fmt.Println(err.Error())
			return
		}
		fmt.Println(string(replyBuf[:n]))

	}
}

func (c *client) sendAndRecvMsg(data []byte) (reply []byte, err error) {
	replyBuf := make([]byte, 1024)
	defer c.Conn.SetDeadline(time.Time{})

	_, err = c.Conn.Write(data)
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	for {
		c.Conn.SetDeadline(time.Now().Add(time.Second * TIMEOUT))
		n, err := c.Conn.Read(replyBuf)
		if err == nil {
			reply = replyBuf[:n]
			break
		}
		fmt.Println(err.Error())
	}
	return
}

func main() {
	m := marshaller{}
	// registry, err := NewRegistry(generateRegistry)
	// if err != nil {
	// 	fmt.Printf("error: %s\n", err.Error())
	// 	return
	// }
	// fmt.Println(reflect.TypeOf("a"))
	// um := unmarshaller{registry}
	printDetails(m)
	// printUnmarshalDetails(um)
	// var c CurrencyType = CurrencyType(1)
	// fmt.Println(reflect.TypeOf(c))
	ClientLoop("localhost:50000")
}
