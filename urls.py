from view import Index, Example, Page, AnotherPage, Contacts

routers = {
    '/': Index(),
    '/examples/': Example(),
    '/page/': Page(),
    '/another_page/': AnotherPage(),
    '/contacts/': Contacts(),
}
