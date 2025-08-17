import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from icons import FontAwesomeIcons, create_icon, get_icon

# Initialize Dash App
app = dash.Dash(__name__)

# Custom index_string to include Font Awesome, Tailwind, and DaisyUI
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Developer Portfolio</title>

        <!-- Font Awesome CDN -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

        <!-- Material Icons -->
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

        <!-- Tailwind CSS CDN -->
        <script src="https://cdn.tailwindcss.com"></script>

        <!-- DaisyUI CDN -->
        <link href="https://cdn.jsdelivr.net/npm/daisyui@2.51.6/dist/full.css" rel="stylesheet" type="text/css" />

        <!-- Tailwind Configuration -->
        <script>
            tailwind.config = {
                content: [
                    "./index.html",
                    "./main.py"
                ],
                theme: {
                    extend: {
                        colors: {
                            'brand': {
                                '50': '#f0f9ff',
                                '100': '#e0f2fe',
                                '200': '#bae6fd',
                                '300': '#7dd3fc',
                                '400': '#38bdf8',
                                '500': '#0ea5e9',
                                '600': '#0284c7',
                                '700': '#0369a1',
                                '800': '#075985',
                                '900': '#0c4a6e'
                            }
                        }
                    }
                },
                plugins: [
                    require('daisyui')
                ]
            }
        </script>

        {%css%}
    </head>
    <body class="bg-base-100">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Main App Layout
app.layout = html.Div([
    # Navbar
    html.Div([
        html.Div([
            # Logo and Name
            html.Div([
                create_icon(FontAwesomeIcons.LAPTOP_CODE,
                            additional_classes="text-2xl mr-2 text-primary"),
                html.Span("Developer Portfolio",
                          className="text-xl font-bold text-primary")
            ], className="flex items-center"),

            # Navigation Links
            html.Div([
                html.A([
                    create_icon(FontAwesomeIcons.HOME,
                                additional_classes="mr-2"),
                    "Home"
                ], href="#", className="btn btn-ghost"),
                html.A([
                    create_icon(FontAwesomeIcons.USER,
                                additional_classes="mr-2"),
                    "About"
                ], href="#", className="btn btn-ghost"),
                html.A([
                    create_icon(FontAwesomeIcons.SKILLS,
                                additional_classes="mr-2"),
                    "Skills"
                ], href="#", className="btn btn-ghost"),
                html.A([
                    create_icon(FontAwesomeIcons.PROJECT,
                                additional_classes="mr-2"),
                    "Projects"
                ], href="#", className="btn btn-ghost"),
            ], className="flex")
        ], className="navbar bg-base-100 shadow-lg container mx-auto")
    ]),

    # Hero Section
    html.Div([
        html.Div([
            # Left Content
            html.Div([
                html.H1([
                    "👋 Hello, I'm ",
                    html.Span("John Doe", className="text-primary")
                ], className="text-5xl font-bold mb-4"),

                html.H2("Software Engineer & Full Stack Developer",
                        className="text-3xl text-secondary mb-6"),

                html.P("Passionate developer creating innovative solutions with cutting-edge technologies.",
                       className="prose lg:prose-xl mb-8"),

                # Social Links
                html.Div([
                    html.A(create_icon(FontAwesomeIcons.GITHUB, additional_classes="text-3xl"),
                           href="https://github.com/yourusername",
                           className="mr-4 hover:text-primary"),
                    html.A(create_icon(FontAwesomeIcons.LINKEDIN, additional_classes="text-3xl"),
                           href="https://linkedin.com/in/yourusername",
                           className="mr-4 hover:text-primary"),
                    html.A(create_icon(FontAwesomeIcons.TWITTER, additional_classes="text-3xl"),
                           href="https://twitter.com/yourusername",
                           className="hover:text-primary")
                ], className="flex items-center mb-8"),

                # Action Buttons
                html.Div([
                    html.Button([
                        create_icon(FontAwesomeIcons.DOWNLOAD, additional_classes="mr-2"),
                        "Download CV"
                    ], className="btn btn-primary mr-4"),
                    html.Button([
                        create_icon(FontAwesomeIcons.ENVELOPE, additional_classes="mr-2"),
                        "Contact Me"
                    ], className="btn btn-outline btn-secondary")
                ])
            ], className="flex-1"),

            # Profile Image
            html.Div([
                html.Div([
                    html.Img(src="/assets/profile.png",
                             className="rounded-full w-64 h-64 object-cover border-4 border-primary"),
                ], className="avatar online")
            ], className="flex-1 flex justify-center items-center")
        ], className="hero min-h-screen container mx-auto px-10 flex")
    ]),

    # Skills Section
    html.Div([
        html.Div([
            html.H2("💻 Technical Skills",
                    className="text-4xl font-bold text-center text-primary mb-12"),

            # Skill Cards
            html.Div([
                # Frontend Skills
                html.Div([
                    html.Div([
                        html.H3([
                            create_icon(FontAwesomeIcons.LAPTOP_CODE, additional_classes="mr-2"),
                            "Frontend"
                        ], className="card-title text-secondary"),
                        html.Div([
                            html.Span([
                                create_icon(FontAwesomeIcons.REACT, additional_classes="mr-2"),
                                "React"
                            ], className="badge badge-primary badge-outline mr-2 mb-2"),
                            html.Span([
                                create_icon(FontAwesomeIcons.CODE, additional_classes="mr-2"),
                                "Vue"
                            ], className="badge badge-primary badge-outline mr-2 mb-2")
                        ])
                    ], className="card-body")
                ], className="card bg-base-100 shadow-xl"),

                # Backend Skills
                html.Div([
                    html.Div([
                        html.H3([
                            create_icon(FontAwesomeIcons.SERVER, additional_classes="mr-2"),
                            "Backend"
                        ], className="card-title text-secondary"),
                        html.Div([
                            html.Span([
                                create_icon(FontAwesomeIcons .NODE_JS, additional_classes="mr-2"),
                                "Node.js"
                            ], className="badge badge-primary badge-outline mr-2 mb-2"),
                            html.Span([
                                create_icon(FontAwesomeIcons.PYTHON, additional_classes="mr-2"),
                                "Django"
                            ], className="badge badge-primary badge-outline mr-2 mb-2")
                        ])
                    ], className="card-body")
                ], className="card bg-base-100 shadow-xl"),

                # Database Skills
                html.Div([
                    html.Div([
                        html.H3([
                            create_icon(FontAwesomeIcons.DATABASE, additional_classes="mr-2"),
                            "Database"
                        ], className="card-title text-secondary"),
                        html.Div([
                            html.Span([
                                create_icon(FontAwesomeIcons.CLOUD, additional_classes="mr-2"),
                                "MongoDB"
                            ], className="badge badge-primary badge-outline mr-2 mb-2"),
                            html.Span([
                                create_icon(FontAwesomeIcons.DATABASE, additional_classes="mr-2"),
                                "PostgreSQL"
                            ], className="badge badge-primary badge-outline mr-2 mb-2")
                        ])
                    ], className="card-body")
                ], className="card bg-base-100 shadow-xl"),
            ], className="grid grid-cols-1 md:grid-cols-3 gap-4")
        ], className="container mx-auto mb-12")
    ]),

    # Projects Section
    html.Div([
        html.H2("📂 Projects", className="text-4xl font-bold text-center text-primary mb-12"),
        html.Div([
            # Project Card Example
            html.Div([
                html.Div([
                    html.H3("Project Title", className="text-xl font-bold"),
                    html.P("Brief description of the project goes here.", className="mb-4"),
                    html.A("View Project", href="#", className="btn btn-primary")
                ], className="card-body")
            ], className="card bg-base-100 shadow-xl p-4")
        ], className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4")
    ], className="container mx-auto mb-12"),

    # Footer
    html.Footer([
        html.Div("© 2023 John Doe. All rights reserved.", className="text-center text-gray-600")
    ], className="py-4 bg-base-200")
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
