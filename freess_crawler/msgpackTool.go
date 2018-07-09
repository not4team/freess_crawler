package main

import (
	"C"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"ss-server/models"

	"github.com/vmihailenco/msgpack"
)

func Marshal(p *models.Package) error {
	b, err := msgpack.Marshal(p)
	if err != nil {
		return err
	}
	err = ioutil.WriteFile(os.Getenv("GOBIN")+"/ss-server/datas", b, 0644)
	if err != nil {
		return err
	}
	return nil
}

//export InsertProfiles
func InsertProfiles(j string) {
	p := new(models.Package)
	err := json.Unmarshal([]byte(j), p)
	if err != nil {
		fmt.Println(err)
	} else {
		err = Marshal(p)
		if err != nil {
			fmt.Println(err)
		}
	}
}

func main() {
	fmt.Println("msgpackTool main")
}
