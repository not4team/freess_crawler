package main

import (
	"C"
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
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

var commonIV = []byte{0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f}

var key = "aljgla.mgh98570fdg;ghjksirl76jnf"

//export AesEncrypt
func AesEncrypt(content string) *C.char {
	// 创建加密算法aes
	c, err := aes.NewCipher([]byte(key))
	if err != nil {
		fmt.Printf("Error: NewCipher(%d bytes) = %s\n", len(key), err)
	}

	//加密字符串
	cfb := cipher.NewCFBEncrypter(c, commonIV)
	ciphertext := make([]byte, len(content))
	cfb.XORKeyStream(ciphertext, []byte(content))
	// fmt.Printf("%s=>%x\n", content, ciphertext)
	ciphertext = Base64Encode(ciphertext)
	return C.CString(string(ciphertext))
}

func AesDecrypt(content string) *C.char {
	text := make([]byte, len(content))
	var err error
	text, err = Base64Decode([]byte(content))
	if err != nil {
		fmt.Println(err)
	}
	// 创建加密算法aes
	c, err := aes.NewCipher([]byte(key))
	if err != nil {
		fmt.Printf("Error: NewCipher(%d bytes) = %s\n", len(key), err)
	}
	// 解密字符串
	decryptText := make([]byte, len(text))
	cfbdec := cipher.NewCFBDecrypter(c, commonIV)
	cfbdec.XORKeyStream(decryptText, []byte(text))
	// fmt.Printf("%x=>%s\n", text, decryptText)
	return C.CString(string(decryptText))
}

func Base64Encode(src []byte) []byte {
	return []byte(base64.StdEncoding.EncodeToString(src))
}

func Base64Decode(src []byte) ([]byte, error) {
	return base64.StdEncoding.DecodeString(string(src))
}

func main() {
	fmt.Println("msgpackTool main")
}
