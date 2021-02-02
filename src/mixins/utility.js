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
      const intDateParsed = Number(intDate) + 10;

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
      let lower, upper;
      if (metric === 'emission change') {
        lower = -0.5;
        upper = 0.5;
      } else {
        lower = -0.0002;
        upper = 0.0002;
      }

      const r = value < 0 ? 0 : 255 * (value / upper) ** 0.25;
      const g = value > 0 ? 0 : 255 * (value / lower) ** 0.25;
      const b = 0;
      return `rgb(${r}, ${g}, ${b})`;
    },
  },
};