// Auto generated file, do not edit
package $package

import java.util.*

private val languages = mutableMapOf<String, Properties>()

fun String.localized(language: String, default: String = "en"): String {

    // lazy load a language
    if (languages[language] == null) {
        val classLoader = LocalizedKeys::class.java.classLoader
        val langStream = classLoader.getResourceAsStream("locale/$language.properties")

        if (langStream == null) {
            // The requested language is not supported. Fallback to 'en'
            return localized(default)
        }

        val properties = Properties()
        properties.load(langStream)
        languages[language] = properties

    }

    var value = languages[language]?.getProperty(this)

    if (value == null && language != "en") {
        // The requested localization key is not supported in the language, fallback to default
        value = localized(default)
    } else if (value == null) {
        // The requested localization key is not supported in the language, fallback to empty string
        value = ""
    }

    return value

}
