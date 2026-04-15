import os
import getpass

print("\n" + "="*40)
print("  🚀 Hugging Face Auto-Deploy Script")
print("="*40 + "\n")

print("Please paste your Hugging Face Access Token below.")
print("(Your token should start with 'hf_'. It will remain completely invisible while you paste it!)\n")

token = getpass.getpass("Paste Token and press Enter: ").strip()

if not token.startswith("hf_"):
    print("\n❌ Error: The token you pasted doesn't seem right. It should start with 'hf_'.")
    print("Please go back to https://huggingface.co/settings/tokens and copy it again!")
else:
    print("\n✅ Token accepted! Uploading your website to the internet...")
    
    # Securely embed the token into the URL structure to bypass Mac Keychain issues
    secure_url = f"https://adrikap:{token}@huggingface.co/spaces/adrikap/AnemiaSense"
    
    command = f"git push --force {secure_url} main"
    
    # Execute the push command
    exit_code = os.system(command)
    
    if exit_code == 0:
        print("\n🎉 SUCCESS! Your website has been uploaded!")
        print("Go check it out here: https://huggingface.co/spaces/adrikap/AnemiaSense")
    else:
        print("\n⚠️  Uh oh, the upload failed. Double check that your token's role was set to 'Write' and not 'Read'!")

print("\n")
