/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        '../../**/*.py'
    ],
    theme: {
        extend: {},
        fontFamily: {
            'sans': ['Raleway', 'sans-serif'],
            'serif': ['Playfair Display', 'serif']
        }
    },
    daisyui: {
        themes: [
            {
                tea_dark: {
                    "primary": "#afe31e",
                    "secondary": "#fb9931",
                    "accent": "#c7c299",
                    "neutral": "#151203",
                    "base-100": "#202d1f",
                    "base-300": "#171d19",
                    "info": "#7fd3ff",
                    "success": "#2c600f",
                    "warning": "#fff3cd",
                    "error": "#e11d48",
                    "--rounded-box": "0.5rem", // border radius rounded-box utility class, used in card and other large boxes
                    "--rounded-btn": "0.25rem", // border radius rounded-btn utility class, used in buttons and similar element
                    "--rounded-badge": "1.9rem", // border radius rounded-badge utility class, used in badges and similar
                    "--animation-btn": "0.25s", // duration of animation when you click on button
                    "--animation-input": "0.2s", // duration of animation for inputs like checkbox, toggle, radio, etc
                    "--btn-focus-scale": "0.95", // scale transform of button when you focus on it
                    "--border-btn": "1px", // border width of buttons
                    "--tab-border": "1px", // border width of tabs
                    "--tab-radius": "0.5rem", // border radius of tabs
                    "body": {
                        "background": "#202d1f",
                        "background": "linear-gradient(180deg, #171d19 0%, #202d1f 100%)",
                    }
                },
                /** 
                tea_light: {
                    "primary": "#97d523",
                    "secondary": "#051a0a",
                    "accent": "#13391d",
                    "neutral": "#151203",
                    "base-100": "#f0e9db",
                    "base-300": "#f3f4f6",
                    "info": "#7fd3ff",
                    "success": "#2c600f",
                    "warning": "#fff3cd",
                    "error": "#e11d48",
                    "--rounded-box": "0.5rem", // border radius rounded-box utility class, used in card and other large boxes
                    "--rounded-btn": "0.25rem", // border radius rounded-btn utility class, used in buttons and similar element
                    "--rounded-badge": "1.9rem", // border radius rounded-badge utility class, used in badges and similar
                    "--animation-btn": "0.25s", // duration of animation when you click on button
                    "--animation-input": "0.2s", // duration of animation for inputs like checkbox, toggle, radio, etc
                    "--btn-focus-scale": "0.95", // scale transform of button when you focus on it
                    "--border-btn": "1px", // border width of buttons
                    "--tab-border": "1px", // border width of tabs
                    "--tab-radius": "0.5rem", // border radius of tabs
                    "body": {
                        "background": "rgb(243,244,246)",
                        "background": "linear-gradient(180deg, rgba(243,244,246,1) 0%, rgba(240,233,219,1) 100%)",
                    }
                },
                **/
            },
        ],
        safelist: [
            'text',
            'textarea'
        ],
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         * require('@tailwindcss/forms'),
         */
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require("daisyui")
    ],
}
