/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        botanical: {
          50: '#F5F9F1',
          100: '#EBF4E5',
          200: '#E0EED4',
          300: '#D2E6C3',
          400: '#B5D69F',
          500: '#8EB872',
          600: '#69944F',
          700: '#4F723B',
          800: '#3A552C',
          900: '#283C1F',
        },
        forest: {
          50: '#F0F6F1',
          100: '#DFEDDF',
          200: '#BEDA BF',
          300: '#94C096',
          400: '#5F9B63',
          500: '#3D7A41',
          600: '#2D6131',
          700: '#234C26',
          800: '#1B3E22', // Primary deep forest green
          900: '#142E19',
          950: '#0B1C0E',
        },
        sage: {
          50: '#F6F9F5',
          100: '#EDF3EC',
          200: '#DCE7DA',
          300: '#C4D5C2',
          400: '#A4BCA1',
          500: '#7F9E7B',
          600: '#62805E',
          700: '#4D644A',
          800: '#3A4B38',
          900: '#2A3629',
        },
        mint: {
          50: '#F2FAF2',
          100: '#E4F4E4',
          200: '#C9EAC9',
          300: '#A3DAA3',
          400: '#73C373',
          500: '#4AA64B',
          600: '#378738',
          700: '#2D6B2D',
          800: '#265427',
          900: '#1F4620',
        },
        cream: {
          50: '#FCFDFB',
          100: '#F7FAF4',
          200: '#EFF5EA',
          300: '#E4EEE0',
          400: '#D4E2CF',
        },
        status: {
          matched: {
            bg: '#D8EED8',
            text: '#1B4A21',
            border: '#B6DEB6',
          },
          missing: {
            bg: '#FDECE8',
            text: '#922E21',
            border: '#F9C9C2',
          },
          warning: {
            bg: '#FEF4DB',
            text: '#7A540E',
            border: '#FBDFA0',
          },
          info: {
            bg: '#EAF3ED',
            text: '#225530',
            border: '#CFE4D6',
          }
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(27, 62, 34, 0.05), 0 2px 6px -1px rgba(27, 62, 34, 0.03)',
        'soft-md': '0 10px 25px -3px rgba(27, 62, 34, 0.07), 0 4px 10px -2px rgba(27, 62, 34, 0.04)',
        'soft-lg': '0 20px 35px -5px rgba(27, 62, 34, 0.08), 0 8px 16px -4px rgba(27, 62, 34, 0.04)',
        'pill': '0 2px 10px rgba(27, 62, 34, 0.06)',
      },
      borderRadius: {
        '4xl': '2rem',
      }
    },
  },
  plugins: [],
}
