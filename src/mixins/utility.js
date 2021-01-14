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
  },
};