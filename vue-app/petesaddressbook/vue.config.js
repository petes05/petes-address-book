const path = require('path');

module.exports = {
	outputDir: path.resolve(__dirname, '../../django-app/petesaddressbook/addressbook/static/addressbook/dist'),
	configureWebpack: {
		optimization: {
		  splitChunks: {
			chunks: "all"
		  }
		}
	}
}