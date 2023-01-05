TEMPLATE = """<html>
    <head>
        <title>Schemas</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <meta charset="utf-8"/>
        <style>
            ::-webkit-scrollbar {
                width: 7px;
                height: 7px;
            }
            ::-webkit-scrollbar-track {
                background: #fff;
            }
            ::-webkit-scrollbar-thumb {
                background: rgb(199, 199, 199);
                border-radius: 15px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgb(184, 184, 184);
            }
        </style>
    </head>
    <body class="flex">
        <div class="flex w-72 fixed px-3 py-4 overflow-y-auto shadow-lg rounded bg-white h-full">
            <div class="flex flex-grow flex-col">
                <nav class="flex-1 space-y-1 bg-white px-2" aria-label="Sidebar">
          
                    {{nav}}

                </nav>
            </div>
        </div>
          
        <main class="flex-grow pl-72">
            {{body}}
        </main>

        <script type="text/javascript">
            document.querySelectorAll("nav button").forEach((button) => {
                const subMenu = document.getElementById(button.getAttribute("data-submenu"));
                const arrow = button.querySelector("svg");

                if (subMenu)
                    subMenu.classList.toggle("hidden");
                
                button.addEventListener("click", () => {
                    if (subMenu)
                        subMenu.classList.toggle("hidden");
                    if (arrow) {
                        arrow.classList.toggle("-rotate-90");
                        arrow.classList.toggle("text-gray-400");
                        arrow.classList.toggle("text-gray-300");
                    }
                });
            });
        </script>
    </body>
</html>"""