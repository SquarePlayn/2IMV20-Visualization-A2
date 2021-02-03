// Fiji has nearly no cases
const MISSING_COUNTRY = 'Fiji';

const COUNTRY_NAME_EXCEPTIONS = {
    'United States of America': 'United States',
    'Dominican Rep.': 'Dominican Republic',
    'Côte d\'Ivoire': 'Cote d\'Ivoire',
    'W. Sahara': 'Morocco',
    'Dem. Rep. Congo': 'Congo (Brazzaville)',
    'Falkland Is.': MISSING_COUNTRY,
    'Greenland': MISSING_COUNTRY,
    'Fr. S. Antarctic Lands': MISSING_COUNTRY,
    'Puerto Rico': 'Dominican Republic',
    'Central African Rep.': 'Central African Republic',
    'Congo': 'Congo (Kinshasa)',
    'Eq. Guinea': 'Equatorial Guinea',
    'eSwatini': 'Eswatini',
    'Palestine': 'Israel',
    'Myanmar': 'Burma',
    'North Korea': MISSING_COUNTRY,
    'South Korea': 'Korea, South',
    'Turkmenistan': 'Uzbekistan',
    'Caledonia': MISSING_COUNTRY,
    'New Caledonia': MISSING_COUNTRY,
    'Solomon Is.': 'Solomon Islands',
    'Taiwan': 'Taiwan*',
    'Antarctica': MISSING_COUNTRY,
    'N. Cyprus': 'Cyprus',
    'Somaliland': 'Somalia',
    'Bosnia and Herz.': 'Bosnia and Herzegovina',
    'Macedonia': 'North Macedonia',
    'S. Sudan': 'South Sudan',
};

function clamp(num, min, max) {
    return num <= min ? min : num >= max ? max : num;
}

export const utility = {
    methods: {
        /**
         * Convert a day integer to the string representation of that day, where 0 maps to the
         * first day in our dataset ("2020-01-22")
         * @param intDate int day index (from 0 to size of dataset)
         * @return string YYYY-MM-DD representation of that day of the year 2020, offset by 22 (start of dataset)
         */
        formatDate(intDate) {
            // Make really sure it's an int (and not e.g. a string)
            const intDateParsed = Number(intDate);

            // Construct date `intDate` days from start of dataset
            const date = new Date('2020-01-22');
            date.setDate(date.getDate() + intDateParsed);

            // Output YYYY-MM-DD representation
            return date.toISOString().split('T')[0];
        },

        convertCountryName(countryName) {
            if (countryName in COUNTRY_NAME_EXCEPTIONS) {
                return COUNTRY_NAME_EXCEPTIONS[countryName];
            } else {
                return countryName;
            }
        },

        /**
         * For a certian value of a metric, get the color to display it as
         * @param value
         * @param metric
         */
        getCountryColor(value, metric) {
            let lower, upper, r_a, g_a, b_a, r_b, g_b, b_b;

            if (metric === 'emission change') {
                lower = -0.35;
                upper = 0.35;
                r_a = 251;
                g_a = 72;
                b_a = 25;
                r_b = 11;
                g_b = 218;
                b_b = 81;
            } else {
                r_a = 0;
                g_a = 0;
                b_a = 0;
                r_b = 250;
                g_b = 235;
                b_b = 215;
            }

            if (metric === 'Recovered') {
                lower = 0;
                upper = 0.0001;
                r_a = 11;
                g_a = 218;
                b_a = 81;
            } else if (metric === 'Deaths') {
                lower = 0;
                upper = 0.000008;
            } else if (metric === 'Confirmed') {
                lower = 0;
                upper = 0.00025;
                r_a = 251;
                g_a = 72;
                b_a = 25;
            }

            const distance = upper - lower;
            const intensity = (clamp(value, lower, upper) - lower) / distance

            return this.interpolate(intensity, r_a, g_a, b_a, r_b, g_b, b_b);
        },

        interpolate(intensity, r_a, g_a, b_a, r_b, g_b, b_b) {
            let r, g, b;

            r = intensity * r_a + (1 - intensity) * r_b;
            g = intensity * g_a + (1 - intensity) * g_b;
            b = intensity * b_a + (1 - intensity) * b_b;

            return `rgb(${r}, ${g}, ${b})`;
        }
    },
};