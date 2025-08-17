// src/main.rs
use iced::widget::{button, column, container, row, scrollable, text, Space};
use iced::{Alignment, Application, Command, Element, Length, Settings, Theme};
use iced::theme;

// Custom styles
#[derive(Default)]
struct NavButtonStyle {
    is_active: bool,
}

impl button::StyleSheet for NavButtonStyle {
    type Style = Theme;

    fn active(&self, style: &Self::Style) -> button::Appearance {
        if self.is_active {
            button::Appearance {
                background: Some(iced::Background::Color(iced::Color::from_rgb(0.2, 0.6, 1.0))),
                text_color: iced::Color::WHITE,
                border_radius: 8.0.into(),
                ..Default::default()
            }
        } else {
            button::Appearance {
                background: Some(iced::Background::Color(iced::Color::TRANSPARENT)),
                text_color: match style {
                    Theme::Dark => iced::Color::WHITE,
                    _ => iced::Color::BLACK,
                },
                border_radius: 8.0.into(),
                ..Default::default()
            }
        }
    }
}

#[derive(Default)]
struct PrimaryButtonStyle;

impl button::StyleSheet for PrimaryButtonStyle {
    type Style = Theme;

    fn active(&self, _style: &Self::Style) -> button::Appearance {
        button::Appearance {
            background: Some(iced::Background::Color(iced::Color::from_rgb(0.2, 0.6, 1.0))),
            text_color: iced::Color::WHITE,
            border_radius: 8.0.into(),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct SecondaryButtonStyle;

impl button::StyleSheet for SecondaryButtonStyle {
    type Style = Theme;

    fn active(&self, _style: &Self::Style) -> button::Appearance {
        button::Appearance {
            background: Some(iced::Background::Color(iced::Color::from_rgba(0.2, 0.6, 1.0, 0.2))),
            text_color: iced::Color::from_rgb(0.2, 0.6, 1.0),
            border_radius: 8.0.into(),
            border_width: 1.0,
            border_color: iced::Color::from_rgb(0.2, 0.6, 1.0),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct ThemeButtonStyle;

impl button::StyleSheet for ThemeButtonStyle {
    type Style = Theme;

    fn active(&self, _style: &Self::Style) -> button::Appearance {
        button::Appearance {
            background: Some(iced::Background::Color(iced::Color::from_rgb(0.1, 0.1, 0.1))),
            text_color: iced::Color::WHITE,
            border_radius: 20.0.into(),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct CardContainerStyle;

impl container::StyleSheet for CardContainerStyle {
    type Style = Theme;

    fn appearance(&self, style: &Self::Style) -> container::Appearance {
        container::Appearance {
            background: Some(iced::Background::Color(match style {
                Theme::Dark => iced::Color::from_rgba(0.1, 0.1, 0.1, 0.5),
                _ => iced::Color::from_rgba(1.0, 1.0, 1.0, 0.8),
            })),
            border_radius: 16.0.into(),
            border_width: 1.0,
            border_color: iced::Color::from_rgba(0.5, 0.5, 0.5, 0.2),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct NavbarContainerStyle;

impl container::StyleSheet for NavbarContainerStyle {
    type Style = Theme;

    fn appearance(&self, style: &Self::Style) -> container::Appearance {
        container::Appearance {
            background: Some(iced::Background::Color(match style {
                Theme::Dark => iced::Color::from_rgba(0.1, 0.1, 0.1, 0.9),
                _ => iced::Color::from_rgba(0.95, 0.95, 0.95, 0.9),
            })),
            border_radius: 16.0.into(),
            border_width: 1.0,
            border_color: iced::Color::from_rgba(0.5, 0.5, 0.5, 0.3),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct HeroContainerStyle;

impl container::StyleSheet for HeroContainerStyle {
    type Style = Theme;

    fn appearance(&self, style: &Self::Style) -> container::Appearance {
        container::Appearance {
            background: Some(iced::Background::Color(match style {
                Theme::Dark => iced::Color::from_rgba(0.05, 0.15, 0.25, 0.3),
                _ => iced::Color::from_rgba(0.9, 0.95, 1.0, 0.5),
            })),
            border_radius: 20.0.into(),
            border_width: 1.0,
            border_color: iced::Color::from_rgba(0.2, 0.6, 1.0, 0.3),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct TechPillStyle;

impl container::StyleSheet for TechPillStyle {
    type Style = Theme;

    fn appearance(&self, _style: &Self::Style) -> container::Appearance {
        container::Appearance {
            background: Some(iced::Background::Color(iced::Color::from_rgba(0.2, 0.6, 1.0, 0.2))),
            border_radius: 12.0.into(),
            border_width: 1.0,
            border_color: iced::Color::from_rgb(0.2, 0.6, 1.0),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct ProgressBarStyle;

impl container::StyleSheet for ProgressBarStyle {
    type Style = Theme;

    fn appearance(&self, style: &Self::Style) -> container::Appearance {
        container::Appearance {
            background: Some(iced::Background::Color(match style {
                Theme::Dark => iced::Color::from_rgba(0.3, 0.3, 0.3, 0.5),
                _ => iced::Color::from_rgba(0.8, 0.8, 0.8, 0.5),
            })),
            border_radius: 4.0.into(),
            ..Default::default()
        }
    }
}

#[derive(Default)]
struct ProgressFillStyle;

impl container::StyleSheet for ProgressFillStyle {
    type Style = Theme;

    fn appearance(&self, _style: &Self::Style) -> container::Appearance {
        container::Appearance {
            background: Some(iced::Background::Color(iced::Color::from_rgb(0.2, 0.6, 1.0))),
            border_radius: 4.0.into(),
            ..Default::default()
        }
    }
}

fn main() -> iced::Result {
    Portfolio::run(Settings {
        window: iced::window::Settings {
            size: (900, 700),
            ..Default::default()
        },
        ..Default::default()
    })
}

#[derive(Debug, Clone)]
enum Message {
    NavigateTo(Section),
    ToggleTheme,
}

#[derive(Debug, Clone, PartialEq)]
enum Section {
    Home,
    About,
    Skills,
    Projects,
    Contact,
}

struct Portfolio {
    current_section: Section,
    theme: Theme,
}

impl Application for Portfolio {
    type Message = Message;
    type Theme = Theme;
    type Executor = iced::executor::Default;
    type Flags = ();

    fn new(_flags: ()) -> (Self, Command<Message>) {
        (
            Portfolio {
                current_section: Section::Home,
                theme: Theme::Dark,
            },
            Command::none(),
        )
    }

    fn title(&self) -> String {
        String::from("Portfolio - John Developer")
    }

    fn update(&mut self, message: Message) -> Command<Message> {
        match message {
            Message::NavigateTo(section) => {
                self.current_section = section;
            }
            Message::ToggleTheme => {
                self.theme = match self.theme {
                    Theme::Light => Theme::Dark,
                    Theme::Dark => Theme::Light,
                    _ => Theme::Dark,
                };
            }
        }
        Command::none()
    }

    fn view(&self) -> Element<Message> {
        let content = column![
            self.navbar(),
            Space::with_height(20),
            self.current_section_view()
        ]
        .spacing(0)
        .align_items(Alignment::Center);

        container(content)
            .width(Length::Fill)
            .height(Length::Fill)
            .into()
    }

    fn theme(&self) -> Theme {
        self.theme.clone()
    }
}

impl Portfolio {
    fn navbar(&self) -> Element<Message> {
        let nav_button = |label: &str, section: Section, current: &Section| {
            button(text(label).size(16))
                .padding([8, 16])
                .style(theme::Button::Custom(Box::new(NavButtonStyle {
                    is_active: *current == section,
                })))
                .on_press(Message::NavigateTo(section))
        };

        let navbar = row![
            nav_button("🏠 Home", Section::Home, &self.current_section),
            nav_button("👤 About", Section::About, &self.current_section),
            nav_button("⚡ Skills", Section::Skills, &self.current_section),
            nav_button("💼 Projects", Section::Projects, &self.current_section),
            nav_button("📞 Contact", Section::Contact, &self.current_section),
            Space::with_width(20),
            button(text("🌙").size(20))
                .padding(8)
                .style(theme::Button::Custom(Box::new(ThemeButtonStyle)))
                .on_press(Message::ToggleTheme),
        ]
        .spacing(8)
        .align_items(Alignment::Center);

        container(navbar)
            .padding(16)
            .style(theme::Container::Custom(Box::new(NavbarContainerStyle)))
            .into()
    }

    fn current_section_view(&self) -> Element<Message> {
        let content = match self.current_section {
            Section::Home => self.home_view(),
            Section::About => self.about_view(),
            Section::Skills => self.skills_view(),
            Section::Projects => self.projects_view(),
            Section::Contact => self.contact_view(),
        };

        scrollable(content).height(Length::Fill).into()
    }

    fn home_view(&self) -> Element<Message> {
        let hero = column![
            text("👨‍💻").size(80),
            Space::with_height(20),
            text("John Developer").size(48).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(10),
            text("Full-Stack Developer & Linux Enthusiast").size(24),
            Space::with_height(20),
            text("Building awesome applications with modern technologies\nArch Linux • Hyprland • Rust • Python • Web Development")
                .size(16)
                .horizontal_alignment(iced::alignment::Horizontal::Center),
            Space::with_height(30),
            row![
                button(text("View Projects").size(16))
                    .padding([12, 24])
                    .style(theme::Button::Custom(Box::new(PrimaryButtonStyle)))
                    .on_press(Message::NavigateTo(Section::Projects)),
                Space::with_width(16),
                button(text("Get In Touch").size(16))
                    .padding([12, 24])
                    .style(theme::Button::Custom(Box::new(SecondaryButtonStyle)))
                    .on_press(Message::NavigateTo(Section::Contact)),
            ]
            .spacing(0)
        ]
        .spacing(0)
        .align_items(Alignment::Center)
        .padding(40);

        container(hero)
            .width(Length::Fill)
            .center_x()
            .center_y()
            .style(theme::Container::Custom(Box::new(HeroContainerStyle)))
            .into()
    }

    fn about_view(&self) -> Element<Message> {
        let content = column![
            text("About Me").size(36).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(20),
            self.card(column![
                text("I'm a passionate developer who loves creating efficient and beautiful applications. I use Arch Linux with Hyprland as my daily driver and enjoy working with modern technologies like Rust, Python, and various frameworks.").size(16),
                Space::with_height(16),
                text("My journey into programming started with curiosity about how things work under the hood. I love the challenge of solving complex problems and the satisfaction of building something that makes people's lives easier.").size(16),
                Space::with_height(16),
                text("When I'm not coding, you can find me contributing to open-source projects, exploring new technologies, or tweaking my Hyprland configuration to perfection.").size(16),
                Space::with_height(20),
                text("Quick Facts").size(20).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
                Space::with_height(10),
                text("🐧 Daily driver: Arch Linux + Hyprland").size(14),
                text("⌨️ Favorite languages: Rust, Python, JavaScript").size(14),
                text("🎯 Focus: Desktop apps & web development").size(14),
                text("☕ Fuel: Coffee and open-source software").size(14),
            ].spacing(4).into())
        ]
        .spacing(0)
        .align_items(Alignment::Center)
        .padding(40);

        container(content).width(Length::Fill).into()
    }

    fn skills_view(&self) -> Element<Message> {
        let prog_skills = column![
            text("Programming Languages").size(20).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(12),
            self.skill_bar("Rust", 85),
            self.skill_bar("Python", 90),
            self.skill_bar("JavaScript", 80),
            self.skill_bar("C++", 70),
        ].spacing(8);

        let tech_skills = column![
            text("Technologies & Tools").size(20).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(12),
            self.skill_bar("Iced/GUI", 80),
            self.skill_bar("Web Dev", 85),
            self.skill_bar("Linux/Bash", 95),
            self.skill_bar("Git", 90),
        ].spacing(8);

        let content = column![
            text("Skills & Technologies").size(36).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(30),
            row![
                self.card(prog_skills.into()),
                Space::with_width(20),
                self.card(tech_skills.into()),
            ]
        ]
        .align_items(Alignment::Center)
        .padding(40);

        container(content).width(Length::Fill).into()
    }

    fn projects_view(&self) -> Element<Message> {
        let projects = column![
            self.project_card(
                "Hyprland Config Manager",
                "A modern GUI application for managing Hyprland configurations with real-time preview and easy customization.",
                &["Rust", "Iced", "TOML", "Linux"]
            ),
            Space::with_height(20),
            self.project_card(
                "System Monitor",
                "Real-time system monitoring dashboard with beautiful charts and system information display.",
                &["Rust", "Iced", "sysinfo", "Charts"]
            ),
            Space::with_height(20),
            self.project_card(
                "Package Manager GUI",
                "Modern package manager interface for Arch Linux with AUR support and dependency visualization.",
                &["Rust", "Iced", "Alpm", "AUR"]
            ),
        ];

        let content = column![
            text("Featured Projects").size(36).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(30),
            projects,
        ]
        .align_items(Alignment::Center)
        .padding(40);

        container(content).width(Length::Fill).into()
    }

    fn contact_view(&self) -> Element<Message> {
        let content = column![
            text("Let's Connect").size(36).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(30),
            self.card(column![
                text("I'm always open to discussing new opportunities,\ncollaborations, or just having a chat about technology!").size(18).horizontal_alignment(iced::alignment::Horizontal::Center),
                Space::with_height(30),
                column![
                    self.contact_item("📧", "john.developer@email.com"),
                    self.contact_item("🐙", "github.com/johndeveloper"),
                    self.contact_item("💼", "linkedin.com/in/johndeveloper"),
                    self.contact_item("🌐", "johndeveloper.dev"),
                ].spacing(12)
            ].align_items(Alignment::Center).into())
        ]
        .align_items(Alignment::Center)
        .padding(40);

        container(content).width(Length::Fill).into()
    }

    fn card<'a>(&self, content: Element<'a, Message>) -> Element<'a, Message> {
        container(content)
            .padding(24)
            .style(theme::Container::Custom(Box::new(CardContainerStyle)))
            .into()
    }

    fn skill_bar(&self, name: &str, level: u8) -> Element<Message> {
        let progress_width = (300.0 * (level as f32 / 100.0)) as u16;
        
        column![
            row![
                text(name).size(14),
                Space::with_width(Length::Fill),
                text(format!("{}%", level)).size(14),
            ],
            Space::with_height(4),
            container(
                container(Space::with_width(progress_width))
                    .style(theme::Container::Custom(Box::new(ProgressFillStyle)))
            )
            .width(300)
            .height(8)
            .style(theme::Container::Custom(Box::new(ProgressBarStyle)))
        ]
        .spacing(0)
        .into()
    }

    fn project_card(&self, title: &str, description: &str, tech: &[&str]) -> Element<Message> {
        let tech_pills = tech.iter().fold(row![], |row, t| {
            row.push(
                container(text(*t).size(12))
                    .padding([4, 8])
                    .style(theme::Container::Custom(Box::new(TechPillStyle)))
            )
        }).spacing(8);

        self.card(column![
            text(title).size(20).style(iced::Color::from_rgb(0.2, 0.6, 1.0)),
            Space::with_height(8),
            text(description).size(14),
            Space::with_height(12),
            tech_pills,
            Space::with_height(16),
            button(text("View on GitHub").size(14))
                .padding([8, 16])
                .style(theme::Button::Custom(Box::new(PrimaryButtonStyle)))
                .on_press(Message::NavigateTo(Section::Projects)) // Placeholder action
        ].spacing(0).into())
    }

    fn contact_item(&self, icon: &str, info: &str) -> Element<Message> {
        row![
            text(icon).size(20),
            Space::with_width(12),
            text(info).size(16),
        ]
        .align_items(Alignment::Center)
        .into()
    }
}
