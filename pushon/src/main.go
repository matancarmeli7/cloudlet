package main

import (
	"fmt"
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"net/http"
	"path/filepath"
	df "pushon/packages/docker_functions"
	"sync"
)

func main() {
	router := gin.Default()
	// Set a lower memory limit for multipart forms (default is 32 MiB)
	router.MaxMultipartMemory = 8 << 20 // 8 MiB
	router.Static("/public", "./public")
	router.StaticFile("/", "./public/html/index.html")
	router.StaticFile("/pushon", "./public/html/pushon.html")
	store := cookie.NewStore([]byte("secret"))
	router.Use(sessions.Sessions("mysession", store))
	router.POST("/upload", func(c *gin.Context) {
		session := sessions.Default(c)
		registryUrl := c.PostForm("registryurl")
		registryUser := c.PostForm("registryuser")
		registryPass := c.PostForm("registrypass")
		var filePaths []string

		// Multipart form
		form, err := c.MultipartForm()
		if err != nil {
			c.String(http.StatusBadRequest, fmt.Sprintf("get form err: %s", err.Error()))
			return
		}

		files := form.File

		for _, file := range files {
            filename := "/tmp/" + filepath.Base(file[0].Filename)
			if err := c.SaveUploadedFile(file[0], filename); err != nil {
				c.String(http.StatusBadRequest, fmt.Sprintf("upload file err: %s", err.Error()))
				return
			}
			filePaths = append(filePaths, filename)
		}

		session.Set("filePaths", filePaths)
		session.Set("registryUrl", registryUrl)
		session.Set("registryUser", registryUser)
		session.Set("registryPass", registryPass)
		session.Save()

		c.Redirect(http.StatusFound, "/pushon")
	})

	router.GET("/ws", func(c *gin.Context) {
		session := sessions.Default(c)
		wshandler(c.Writer, c.Request, session)
	})

	router.Run(":8080")
}

var wsupgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

func wshandler(w http.ResponseWriter, r *http.Request, sess sessions.Session) {
	conn, err := wsupgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Println("Failed to set websocket upgrade: %+v", err)
		return
	}

	fp, ok := sess.Get("filePaths").([]string)
	if !ok {
		return
	}

	var wg sync.WaitGroup
	var mutex = &sync.Mutex{}
	registryName, ok := sess.Get("registryUrl").(string)
	registryUser, ok := sess.Get("registryUser").(string)
	registryPass, ok := sess.Get("registryPass").(string)

	for _, file := range fp {
		wg.Add(1)
		go df.LoadTagAndPush(file, registryName, registryUser, registryPass, &wg, mutex, conn)
	}

	wg.Wait()

	mutex.Lock()
	conn.WriteMessage(websocket.TextMessage, []byte("Pushon ended! Have a lovely day!"))
	mutex.Unlock()
	conn.Close()

}
