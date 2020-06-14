package docker_functions

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/client"
	"github.com/gorilla/websocket"
	"io"
	"io/ioutil"
	"os"
	"strings"
	"sync"
)

func LoadTagAndPush(imagePath string, registryName string, registryUser string, registryUserPass string, wg *sync.WaitGroup, mutex *sync.Mutex, conn *websocket.Conn) (err error) {
	defer mutex.Unlock()
	mutex.Lock()
	err = conn.WriteMessage(websocket.TextMessage, []byte("Started loading "+imagePath))
	mutex.Unlock()
	if err != nil {
		wg.Done()
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}

	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		wg.Done()
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}
	defer cli.Close()

	f, err := os.Open(imagePath)
	if err != nil {
		wg.Done()
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}
	defer f.Close()

	i, err := cli.ImageLoad(ctx, f, true)
	defer i.Body.Close()

	data, err := ioutil.ReadAll(i.Body)
	if err != nil {
		wg.Done()
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}

	imageName := string(data)[25 : len(data)-6]
	var cleanImageName string
	if strings.Contains(imageName, "redhat") {
		cleanImageName = (strings.SplitN(imageName, "/", 2))[1]
	} else {
		cleanImageName = imageName
	}
	if !strings.HasSuffix(registryName, "/") {
		registryName = registryName + "/"
	}
	newImageName := registryName + cleanImageName
	err = cli.ImageTag(ctx, imageName, newImageName)
	if err != nil {
		wg.Done()
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}

	mutex.Lock()
	err = conn.WriteMessage(websocket.TextMessage, []byte("Successfully loaded "+imageName))
	mutex.Unlock()
	if err != nil {
		wg.Done()
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}

	err = PushImage(newImageName, registryUser, registryUserPass, wg, mutex, conn)
	if err != nil {
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}
	mutex.Lock()
	return
}

func PushImage(imageName string, registryUser string, registryUserPass string, wg *sync.WaitGroup, mutex *sync.Mutex, conn *websocket.Conn) (err error) {
	defer wg.Done()
	defer mutex.Unlock()

	mutex.Lock()
	err = conn.WriteMessage(websocket.TextMessage, []byte("Starting pushing "+imageName))
	mutex.Unlock()
	if err != nil {
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}

	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}
	defer cli.Close()

	authConfig := types.AuthConfig{
		Username: registryUser,
		Password: registryUserPass,
	}
	encodedJSON, err := json.Marshal(authConfig)
	authStr := base64.URLEncoding.EncodeToString(encodedJSON)
	pushOptions := types.ImagePushOptions{RegistryAuth: authStr}
	p, err := cli.ImagePush(ctx, imageName, pushOptions)
	if err != nil {
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}
	defer p.Close()
	_, err = io.Copy(ioutil.Discard, p)
	if err != nil {
		mutex.Lock()
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}

	mutex.Lock()
	err = conn.WriteMessage(websocket.TextMessage, []byte("Successfully pushed "+imageName))
	if err != nil {
		conn.WriteMessage(websocket.TextMessage, []byte(err.Error()))
		return
	}

	return
}

func main() {
}
