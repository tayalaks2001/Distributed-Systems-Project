package main

import (
	"fmt"
	"net"
	"os"
	"reflect"
	"time"
)

const TIMEOUT = 5
var message_id int = 0

type client struct {
	net.Conn
}

func menu() (option uint64) {
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

func getInt() (val uint64) {
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

func getFloat() (val float64) {
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

func printCurrencyTypeOptions() {
	fmt.Println("SGD: 0")
	fmt.Println("USD: 1")
	fmt.Println("INR: 2")
}

func checkPasswordLength(password string) bool{
	return len(password) != 11
}

func createMessage(option uint64) (msg Marshalable) {

	switch option {
	case 1:
		{
			fmt.Println("Creating new account...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter 11-character Password")
			var password string = ""
			for checkPasswordLength(password) {
				password = getString()
			}
			fmt.Println("Enter Initial Balance")
			balance := getFloat()
			fmt.Println("Enter Currency Type")
			printCurrencyTypeOptions()
			currencyType := getInt()
			msg = CreateBankAccountMessage{name, password, balance, CurrencyType(currencyType)}
		}
	case 2:
		{
			fmt.Println("Closing account...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter 11-character Password")
			var password string = ""
			for checkPasswordLength(password) {
				password = getString()
			}
			msg = CloseAccountMessage{name, accNum, password}
		}
	case 3:
		{
			fmt.Println("Depositing money...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter 11-character Password")
			var password string = ""
			for checkPasswordLength(password) {
				password = getString()
			}
			fmt.Println("Enter Currency Type")
			printCurrencyTypeOptions()
			currencyType := getInt()
			fmt.Println("Enter Ammount")
			ammount := getFloat()
			msg = DepositMessage{DWBaseMessage{name, accNum, password, CurrencyType(currencyType), ammount}}
		}
	case 4:
		{
			fmt.Println("Withdrawing money...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter 11-character Password")
			var password string = ""
			for checkPasswordLength(password) {
				password = getString()
			}
			fmt.Println("Enter Currency Type")
			printCurrencyTypeOptions()
			currencyType := getInt()
			fmt.Println("Enter Ammount")
			ammount := getFloat()
			msg = WithdrawMessage{DWBaseMessage{name, accNum, password, CurrencyType(currencyType), ammount}}
		}
	case 5:
		{
			fmt.Println("Querying balance...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter 11-character Password")
			var password string = ""
			for checkPasswordLength(password) {
				password = getString()
			}
			msg = QueryBalanceMessage{name, accNum, password}
		}
	case 6:
		{
			fmt.Println("Transfering money...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter your Account Number")
			accNum := getInt()
			fmt.Println("Enter 11-character Password")
			var password string = ""
			for checkPasswordLength(password) {
				password = getString()
			}
			fmt.Println("Enter Currency Type")
			printCurrencyTypeOptions()
			currencyType := getInt()
			fmt.Println("Enter Ammount")
			ammount := getFloat()
			fmt.Println("Enter Recepient Account Number")
			rcvAccNum := getInt()
			msg = TransferMessage{name, accNum, password, CurrencyType(currencyType), ammount, rcvAccNum}
		}	

	case 7:
		{
			fmt.Println("Requesting to monitor...")
			fmt.Println("Enter Name")
			name := getString()
			fmt.Println("Enter Account Number")
			accNum := getInt()
			fmt.Println("Enter 11-character Password")
			var password string = ""
			for checkPasswordLength(password) {
				password = getString()
			}
			fmt.Println("Enter Duration in minutes")
			duration := getInt()
			msg = RegisterMonitorMessage{name, accNum, password, duration}
		}
	}
	return msg
}

func ClientLoop(address string) {
	var err error
	var reply []byte
	c := &client{}
	m := marshaller{}
	registry, err := NewRegistry(generateRegistry)
	if err != nil {
		fmt.Printf("error: %s\n", err.Error())
		return
	}
	fmt.Println(reflect.TypeOf("a"))
	um := unmarshaller{registry}

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
		data = compile_message(m, message_id, msg)

		var recvd_message_id int = -100
		var response Marshalable = nil
		for message_id != recvd_message_id {
			reply, err = c.sendAndRecvMsg(data)
			if err == nil {
				// fmt.Println("Raw reply: " + string(reply))
				recvd_message_id, response = decompile_message(um, reply)
			}
		} 	
		message_id += 1
		fmt.Println("Message from Server:")
		fmt.Println(response.(MessageResponse).extractMssg())
		if option == 7 {
			// check if response recvd was correct
			c.monitor(um, int(msg.(RegisterMonitorMessage).durationMinutes))
		}
	}
}

func (c *client) monitor(um unmarshal_functions, duration int) {
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
		recvd_message_id, response := decompile_message(um, replyBuf)
		fmt.Println(recvd_message_id)
		fmt.Println(response.(MessageResponse).extractMssg())
		fmt.Println(string(replyBuf[:n]))
	}
}

func (c *client) sendAndRecvMsg(data []byte) (reply []byte, err error) {

	defer c.Conn.SetReadDeadline(time.Time{})
	for {
		replyBuf := make([]byte, 1024)
		_, err = c.Conn.Write(data)
		if err != nil {
			fmt.Println(err.Error())
			return
		}
		c.Conn.SetReadDeadline(time.Now().Add(time.Second * TIMEOUT))
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
	
	// registry, err := NewRegistry(generateRegistry)
	// if err != nil {	// 	fmt.Printf("error: %s\n", err.Error())
	// 	return
	// }
	// fmt.Println(reflect.TypeOf("a"))
	// um := unmarshaller{registry}
	//printDetails(m)
	// printUnmarshalDetails(um)
	// var c CurrencyType = CurrencyType(1)
	// fmt.Println(reflect.TypeOf(c))
	ClientLoop("192.168.131.109:2222")
}
