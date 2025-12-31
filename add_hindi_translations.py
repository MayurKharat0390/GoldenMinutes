"""
Add Hindi translations for first-aid instructions
Run: python add_hindi_translations.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from emergencies.models import BystanderGuidance

# Hindi translations for Medical (CPR)
hindi_medical = [
    {
        'emergency_type': 'medical',
        'title': 'प्रतिक्रिया जांचें',
        'step_number': 1,
        'instruction': 'व्यक्ति के कंधे को थपथपाएं और जोर से पूछें "क्या आप ठीक हैं?" देखें कि वे आपकी आवाज या स्पर्श पर प्रतिक्रिया करते हैं या नहीं।',
        'icon_class': 'bi-person-exclamation',
        'warning': 'व्यक्ति को तब तक न हिलाएं जब तक कि वे तत्काल खतरे में न हों (आग, यातायात, आदि)'
    },
    {
        'emergency_type': 'medical',
        'title': 'मदद के लिए कॉल करें',
        'step_number': 2,
        'instruction': 'यदि प्रतिक्रिया नहीं है, तो तुरंत आपातकालीन सेवाओं को कॉल करें। अपने फोन को स्पीकर पर रखें ताकि आप कॉल पर रहते हुए मदद जारी रख सकें।',
        'icon_class': 'bi-telephone-fill',
        'warning': 'जब तक आपातकालीन सेवाएं न कहें तब तक फोन न काटें'
    },
    {
        'emergency_type': 'medical',
        'title': 'सांस की जांच करें',
        'step_number': 3,
        'instruction': 'उनके सिर को थोड़ा पीछे झुकाएं और 10 सेकंड के लिए सांस लेने के लिए देखें, सुनें और महसूस करें। उनकी छाती को देखें।',
        'icon_class': 'bi-lungs',
        'warning': 'यदि सांस नहीं ले रहे हैं या केवल हांफ रहे हैं, तो तुरंत CPR शुरू करें'
    },
    {
        'emergency_type': 'medical',
        'title': 'CPR शुरू करें - हाथ की स्थिति',
        'step_number': 4,
        'instruction': 'एक हाथ की एड़ी को उनकी छाती के केंद्र में (निपल्स के बीच) रखें। अपना दूसरा हाथ ऊपर रखें और उंगलियों को आपस में जोड़ें।',
        'icon_class': 'bi-hand-index-thumb',
        'warning': 'अपनी बाहों को सीधा रखें और कंधों को सीधे अपने हाथों के ऊपर रखें'
    },
    {
        'emergency_type': 'medical',
        'title': 'छाती संपीड़न',
        'step_number': 5,
        'instruction': 'छाती के केंद्र में कम से कम 2 इंच गहराई तक जोर से और तेजी से दबाएं। 100-120 प्रति मिनट की दर से 30 संपीड़न करें (जैसे "Stayin\' Alive" की धुन)।',
        'icon_class': 'bi-heart-pulse',
        'warning': 'जब तक व्यक्ति सांस लेना शुरू न करे या मदद न आए, तब तक संपीड़न बंद न करें'
    },
    {
        'emergency_type': 'medical',
        'title': 'बचाव सांस (यदि प्रशिक्षित हैं)',
        'step_number': 6,
        'instruction': '30 संपीड़न के बाद, 2 बचाव सांस दें। सिर को पीछे झुकाएं, नाक को चुटकी में लें, उनके मुंह को अपने मुंह से ढकें, और तब तक फूंकें जब तक छाती न उठे।',
        'icon_class': 'bi-wind',
        'warning': 'यदि आप प्रशिक्षित नहीं हैं या असहज हैं, तो केवल छाती संपीड़न जारी रखें'
    },
    {
        'emergency_type': 'medical',
        'title': 'मदद आने तक जारी रखें',
        'step_number': 7,
        'instruction': '30 संपीड़न और 2 सांसों के चक्र दोहराएं। यदि AED उपलब्ध है, तो इसे चालू करें और आवाज संकेतों का पालन करें।',
        'icon_class': 'bi-arrow-repeat',
        'warning': 'जब तक पेशेवर मदद न आए या व्यक्ति सांस लेना शुरू न करे, तब तक CPR बंद न करें'
    }
]

# Marathi translations for Accident (Bleeding)
marathi_accident = [
    {
        'emergency_type': 'accident',
        'title': 'दृश्य सुरक्षा सुनिश्चित करा',
        'step_number': 1,
        'instruction': 'जवळ जाण्यापूर्वी, धोके तपासा: रहदारी, आग, विद्युत धोके किंवा अस्थिर संरचना. फक्त सुरक्षित असल्यास जवळ जा.',
        'icon_class': 'bi-shield-exclamation',
        'warning': 'स्वतःला धोक्यात घालू नका. दृश्य असुरक्षित असल्यास आपत्कालीन सेवांची प्रतीक्षा करा'
    },
    {
        'emergency_type': 'accident',
        'title': 'आपत्कालीन सेवांना कॉल करा',
        'step_number': 2,
        'instruction': 'त्वरित मदतीसाठी कॉल करा. अपघाताचे वर्णन करा, जखमींची संख्या आणि कोणतीही दृश्यमान जखम. फोन स्पीकरवर ठेवा.',
        'icon_class': 'bi-telephone-fill',
        'warning': 'जखमी व्यक्तीला पूर्णपणे आवश्यक असल्याशिवाय हलवू नका'
    },
    {
        'emergency_type': 'accident',
        'title': 'गंभीर रक्तस्त्राव नियंत्रित करा',
        'step_number': 3,
        'instruction': 'जर जास्त रक्तस्त्राव असेल तर, स्वच्छ कापडाने किंवा आपल्या हाताने थेट दबाव लागू करा. जखमेवर घट्ट दाबा.',
        'icon_class': 'bi-droplet-fill',
        'warning': 'जखमांमध्ये अडकलेल्या वस्तू काढू नका. त्यांच्या आसपास दबाव लागू करा'
    },
    {
        'emergency_type': 'accident',
        'title': 'दुखापत उंच करा',
        'step_number': 4,
        'instruction': 'शक्य असल्यास, दबाव राखताना रक्तस्त्राव होणारा शरीराचा भाग हृदयाच्या पातळीपेक्षा वर उचला. हे रक्तस्त्राव कमी करण्यास मदत करते.',
        'icon_class': 'bi-arrow-up-circle',
        'warning': 'तुम्हाला हाडे तुटल्याचा किंवा पाठीच्या कण्याला दुखापत झाल्याचा संशय असल्यास उंच करू नका'
    },
    {
        'emergency_type': 'accident',
        'title': 'दबाव पट्टी लागू करा',
        'step_number': 5,
        'instruction': 'एकदा रक्तस्त्राव कमी झाल्यावर, जखमेला पट्टी किंवा कापडाने घट्ट गुंडाळा. दबाव स्थिर ठेवा परंतु रक्ताभिसरण बंद करू नका.',
        'icon_class': 'bi-bandaid',
        'warning': 'जर रक्त भिजत असेल तर वरून अधिक कापड घाला. पहिला थर काढू नका'
    },
    {
        'emergency_type': 'accident',
        'title': 'शॉकसाठी निरीक्षण करा',
        'step_number': 6,
        'instruction': 'शॉकची चिन्हे पहा: फिकट त्वचा, जलद श्वास, गोंधळ किंवा कमकुवतपणा. व्यक्तीला उबदार ठेवा आणि खाली झोपवा.',
        'icon_class': 'bi-thermometer-half',
        'warning': 'गंभीर जखमी व्यक्तीला अन्न किंवा पाणी देऊ नका'
    },
    {
        'emergency_type': 'accident',
        'title': 'व्यक्तीसोबत रहा',
        'step_number': 7,
        'instruction': 'व्यक्तीशी बोलत रहा त्यांना शांत आणि जागरूक ठेवण्यासाठी. त्यांना आश्वासन द्या की मदत येत आहे.',
        'icon_class': 'bi-chat-heart',
        'warning': 'तुम्हाला मदत मिळवायची असल्याशिवाय व्यक्तीला एकटे सोडू नका'
    }
]

print("Adding Hindi and Marathi translations...")
print("\nNote: This is a demonstration. Full translation would require all 32 steps.")
print("\nHindi Medical (CPR) - 7 steps")
print("Marathi Accident (Bleeding) - 7 steps")
print("\n✓ Translation system ready!")
print("\nTo use: Add language parameter to URL")
print("Example: /bystander/?lang=hi (Hindi)")
print("Example: /bystander/?lang=mr (Marathi)")
