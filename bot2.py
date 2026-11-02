import discord
from discord.ext import commands
from discord import ui, ButtonStyle, TextStyle

# Mendefinisikan jendela modal
class TestModal(ui.Modal, title='Judul Test'):
    field_1 = ui.TextInput(label='Teks Pendek')
    field_2 = ui.TextInput(label='Teks Panjang', style=TextStyle.paragraph)

    # Metode yang dipanggil saat modal dikirim (tombol Submit ditekan)
    async def on_submit(self, interaction: discord.Interaction):
        # Memperbarui pesan tempat tombol berada dengan data dari modal
        await interaction.response.edit_message(
            content=f'Teks Pendek: {self.field_1.value}\nTeks Panjang: {self.field_2.value}'
        )

# Mendefinisikan tombol
class TestButton(ui.Button):
    def _init_(self, label="Tombol Test", style=ButtonStyle.blurple, row=0):
        super()._init_(label=label, style=style, row=row)

    # Metode yang dipanggil saat tombol ditekan
    async def callback(self, interaction: discord.Interaction):
        # 1. Mengubah warna tombol setelah ditekan menjadi abu-abu
        self.style = ButtonStyle.gray
        # Menonaktifkan tombol agar tidak bisa ditekan dua kali (opsional namun disarankan)
        self.disabled = True 
        
        # 2. WAJIB: Kirim modal sebagai respons utama interaksi tombol terlebih dahulu
        await interaction.response.send_modal(TestModal())
        
        # 3. Kirim pesan tambahan di latar belakang (Gunakan interaction.followup)
        # Mengirim pesan pribadi (DM) ke pengguna
        await interaction.user.send("Kamu telah menekan tombol dan membuka modal!")
        # Mengirim pesan ke channel tempat tombol ditekan
        await interaction.followup.send("Tombol telah diproses, silakan isi modal yang muncul.", ephemeral=True)
        
        # 4. Perbarui tampilan tombol yang berubah warna di Discord
        await interaction.message.edit(view=self.view)

# Mendefinisikan tampilan dengan tombol
class TestView(ui.View):
    def _init_(self):
        super()._init_()
        self.add_item(TestButton(label="Tombol Test"))

# Pengaturan bot (Pastikan message_content aktif jika menggunakan command prefix)
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Berhasil login sebagai {bot.user}')

@bot.command()
async def test(ctx):
    # Mengirim pesan dengan tampilan yang berisi tombol
    await ctx.send("Tekan tombol di bawah ini:", view=TestView())

# bot.run('TOKEN_KAMU')
# Menjalankan bot dengan token
