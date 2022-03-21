package main

type TransferMessage struct {
	name            string
	accNum          int
	password        string
	currencyType    int
	transferAmount  float64
	recipientAccNum int
}
