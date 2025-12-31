import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from emergencies.models import BystanderGuidance

# Add Hindi translations for Medical Emergency (CPR)
hindi_medical_steps = [
    {
        'step_number': 1,
        'title': 'सुरक्षा की जांच करें',
        'instruction': 'सुनिश्चित करें कि क्षेत्र सुरक्षित है। यदि कोई खतरा है (आग, यातायात, रसायन), तो पहले उसे दूर करें या मदद के लिए प्रतीक्षा करें।',
        'icon_class': 'bi-shield-check',
        'warning': 'यदि क्षेत्र असुरक्षित है तो खुद को खतरे में न डालें'
    },
    {
        'step_number': 2,
        'title': 'प्रतिक्रिया की जांच करें',
        'instruction': 'व्यक्ति के कंधों को धीरे से हिलाएं और जोर से पूछें "क्या आप ठीक हैं?" यदि कोई प्रतिक्रिया नहीं है, तो तुरंत मदद के लिए चिल्लाएं।',
        'icon_class': 'bi-person-raised-hand',
        'warning': ''
    },
    {
        'step_number': 3,
        'title': 'आपातकालीन सेवाओं को कॉल करें',
        'instruction': 'किसी को 108 (एम्बुलेंस) पर कॉल करने के लिए कहें। यदि अकेले हैं, तो खुद कॉल करें और स्पीकर पर रखें।',
        'icon_class': 'bi-telephone-fill',
        'warning': 'CPR शुरू करने से पहले हमेशा आपातकालीन सेवाओं को कॉल करें'
    },
    {
        'step_number': 4,
        'title': 'वायुमार्ग खोलें',
        'instruction': 'व्यक्ति को उनकी पीठ के बल लिटाएं। एक हाथ माथे पर रखें, दूसरे से ठुड्डी उठाएं। सिर को धीरे से पीछे झुकाएं।',
        'icon_class': 'bi-lungs',
        'warning': 'यदि गर्दन की चोट का संदेह है तो सिर को न हिलाएं'
    },
    {
        'step_number': 5,
        'title': 'सांस की जांच करें',
        'instruction': '10 सेकंड के लिए देखें, सुनें और महसूस करें। छाती के उठने, सांस की आवाज़ या गाल पर हवा की जांच करें।',
        'icon_class': 'bi-wind',
        'warning': ''
    },
    {
        'step_number': 6,
        'title': 'छाती संपीड़न शुरू करें',
        'instruction': 'छाती के केंद्र में अपने हाथों की एड़ी रखें। हाथों को सीधा रखें। कम से कम 5 सेमी गहराई तक तेज़ और कठोर दबाएं। प्रति मिनट 100-120 संपीड़न की दर बनाए रखें।',
        'icon_class': 'bi-heart-pulse-fill',
        'warning': 'संपीड़न के बीच छाती को पूरी तरह से वापस आने दें'
    },
]

# Add Marathi translations for Medical Emergency (CPR)
marathi_medical_steps = [
    {
        'step_number': 1,
        'title': 'सुरक्षा तपासा',
        'instruction': 'क्षेत्र सुरक्षित आहे याची खात्री करा। जर कोणताही धोका असेल (आग, रहदारी, रसायने), प्रथम तो दूर करा किंवा मदतीची प्रतीक्षा करा।',
        'icon_class': 'bi-shield-check',
        'warning': 'जर क्षेत्र असुरक्षित असेल तर स्वतःला धोक्यात घालू नका'
    },
    {
        'step_number': 2,
        'title': 'प्रतिसाद तपासा',
        'instruction': 'व्यक्तीचे खांदे हलकेच हलवा आणि मोठ्याने विचारा "तुम्ही ठीक आहात का?" जर कोणताही प्रतिसाद नसेल, तर त्वरित मदतीसाठी ओरडा।',
        'icon_class': 'bi-person-raised-hand',
        'warning': ''
    },
    {
        'step_number': 3,
        'title': 'आपत्कालीन सेवांना कॉल करा',
        'instruction': 'कोणाला तरी 108 (रुग्णवाहिका) वर कॉल करण्यास सांगा। जर एकटे असाल, तर स्वतः कॉल करा आणि स्पीकरवर ठेवा।',
        'icon_class': 'bi-telephone-fill',
        'warning': 'CPR सुरू करण्यापूर्वी नेहमी आपत्कालीन सेवांना कॉल करा'
    },
    {
        'step_number': 4,
        'title': 'वायुमार्ग उघडा',
        'instruction': 'व्यक्तीला त्यांच्या पाठीवर झोपवा. एक हात कपाळावर ठेवा, दुसऱ्याने हनुवटी उचला. डोके हळूच मागे झुकवा।',
        'icon_class': 'bi-lungs',
        'warning': 'जर मानेच्या दुखापतीचा संशय असेल तर डोके हलवू नका'
    },
    {
        'step_number': 5,
        'title': 'श्वास तपासा',
        'instruction': '10 सेकंदांसाठी पहा, ऐका आणि जाणवा. छातीच्या वर येण्याची, श्वासाच्या आवाजाची किंवा गालावर हवेची तपासणी करा।',
        'icon_class': 'bi-wind',
        'warning': ''
    },
    {
        'step_number': 6,
        'title': 'छाती संकुचन सुरू करा',
        'instruction': 'छातीच्या मध्यभागी आपल्या हातांची टाच ठेवा. हात सरळ ठेवा. किमान 5 सेमी खोलीपर्यंत जलद आणि कठोर दाबा. प्रति मिनिट 100-120 संकुचनांचा दर राखा।',
        'icon_class': 'bi-heart-pulse-fill',
        'warning': 'संकुचनांदरम्यान छाती पूर्णपणे परत येऊ द्या'
    },
]

# Add translations to database
print("Adding Hindi translations for Medical Emergency (CPR)...")
for step in hindi_medical_steps:
    BystanderGuidance.objects.create(
        emergency_type='medical',
        language='hi',
        **step
    )
print(f"✓ Added {len(hindi_medical_steps)} Hindi steps")

print("\nAdding Marathi translations for Medical Emergency (CPR)...")
for step in marathi_medical_steps:
    BystanderGuidance.objects.create(
        emergency_type='medical',
        language='mr',
        **step
    )
print(f"✓ Added {len(marathi_medical_steps)} Marathi steps")

print("\n✅ Translations added successfully!")
print("\nNow bystanders can:")
print("1. Select their preferred language")
print("2. See first-aid instructions in Hindi or Marathi")
print("3. Listen to voice guidance in their language")
