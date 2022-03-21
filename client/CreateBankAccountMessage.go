package main

type CreateBankAccountMessage struct {
	name         string
	accNum       int
	password     string
	currencyType int
}
