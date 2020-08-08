/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package main

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing a car
type SmartContract struct {
	contractapi.Contract
}

// Car describes basic details of what makes up a car
type InMetaData struct {
	From   string `json:"from"`
	To  string `json:"to"`
	Cid string `json:"cid"`
}


type ExMetaData struct {
	Src string `json:"src"`
	Dest string `json:"dest"`
	From   string `json:"from"`
	To  string `json:"to"`
	Cid string `json:"cid"`
}


// InitLedger adds a base set of cars to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	metadatas := []InMetaData{
		InMetaData{From: "Org1", To: "Prius", Cid: "1234"},
		InMetaData{From: "BKHN", To: "Mustang", Cid: "4567"},
	}

	for i := range metadatas {
		dataAsBytes, _ := json.Marshal(metadatas[i])
		err := ctx.GetStub().PutState(metadatas[i].To+metadatas[i].Cid, dataAsBytes)
		if err != nil {
			return fmt.Errorf("Failed to put to world state. %s", err.Error())
		}
	}

	return nil
}

// adds a new internal metadata to the world state with given details
func (s *SmartContract) CreateInMetaData(ctx contractapi.TransactionContextInterface, key string, from string, cid string, to string) error {
	metadata := InMetaData{
		From:   from,
		Cid:  cid,
		To: to,
	}

	dataAsBytes, _ := json.Marshal(metadata)

	return ctx.GetStub().PutState(key, dataAsBytes)
}

// query metadata returns the metadata stored in the world state with given id
func (s *SmartContract) QueryInMetaData(ctx contractapi.TransactionContextInterface, key string) (*InMetaData, error) {
	dataAsBytes, err := ctx.GetStub().GetState(key)

	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}

	if dataAsBytes == nil {
		return nil, fmt.Errorf("%s does not exist", key)
	}

	metadata := new(InMetaData)
	_ = json.Unmarshal(dataAsBytes, metadata)

	return metadata, nil
}




// adds a new internal metadata to the world state with given details
func (s *SmartContract) CreateExMetaData(ctx contractapi.TransactionContextInterface, key string, src string, dest string, from string, cid string, to string) error {
	metadata := ExMetaData{
		Src: src,
		Dest: dest,
		From:   from,
		Cid:  cid,
		To: to,
	}

	dataAsBytes, _ := json.Marshal(metadata)

	return ctx.GetStub().PutState(key, dataAsBytes)
}

// query metadata returns the car stored in the world state with given id
func (s *SmartContract) QueryExMetaData(ctx contractapi.TransactionContextInterface, key string) (*ExMetaData, error) {
	dataAsBytes, err := ctx.GetStub().GetState(key)

	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}

	if dataAsBytes == nil {
		return nil, fmt.Errorf("%s does not exist", key)
	}

	metadata := new(ExMetaData)
	_ = json.Unmarshal(dataAsBytes, metadata)

	return metadata, nil
}



func main() {

	chaincode, err := contractapi.NewChaincode(new(SmartContract))

	if err != nil {
		fmt.Printf("Error create fabcar chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting fabcar chaincode: %s", err.Error())
	}
}
