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

func ClientLoop(address string) {
	var err error
	c := &client{}

	c.Conn, err = net.Dial("udp", address)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(-1)
	}

	// for {

	// send some stuff
	// menu ...

	// normal messages
	msg := []byte("Hello world!")
	reply, err := c.sendAndRecvMsg(msg)
	if err == nil {
		fmt.Println(string(reply))
	}

	msg = []byte("monitor")
	reply, err = c.sendAndRecvMsg(msg)
	if err == nil {
		fmt.Println(string(reply))
	}

	c.monitor(1)

	// }

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
