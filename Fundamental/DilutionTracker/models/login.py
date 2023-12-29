class login:
    def __init__(self, page):
        self.page = page
        self.email = self.page.locator('input[name="email"]')
        self.password = page.locator('input[name="password"]')
        self.btn = page.locator('button:has-text("Sign in")')

    async def login(self):
        await self.page.goto("https://dilutiontracker.com/login")
        await self.email.fill("ronaldchibulu0812@gmail.com")
        await self.password.fill("Xi2pthf2.")
        await self.btn.click()
        await self.page.wait_for_url("https://dilutiontracker.com/app")