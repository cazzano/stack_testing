package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	app.Get("/api/hello", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"message": "hello hi",
		})
	})

	err := app.Listen(":8000")
	if err != nil {
		log.Fatal(err)
	}
}
