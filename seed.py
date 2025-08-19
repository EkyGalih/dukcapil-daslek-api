import asyncio
import random
from datetime import datetime
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine, AsyncSessionLocal, Base
from app.models import (
    User, Penduduk, Keluarga, AsetKeluarga, Pendidikan,
    Kesehatan, LahanKomoditas, Pendataan
)

faker = Faker("id_ID")


async def seed_users(session: AsyncSession, n=10):
    users = [
        User(
            username=faker.user_name(),
            email=faker.email(),
            full_name=faker.name(),
            hashed_password="hashed_password",
            role=random.choice(["admin", "user"]),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for _ in range(n)
    ]
    session.add_all(users)
    await session.commit()


async def seed_keluargas(session: AsyncSession, n=20):
    keluargas = [
        Keluarga(
            nomor=str(faker.random_number(digits=5)),
            nomor_kk=str(faker.unique.random_number(digits=16)),
            nama_kepala_keluarga=faker.name(),
            dusun=faker.city(),
            rw=str(random.randint(1, 5)),
            rt=str(random.randint(1, 10)),
            nomor_rumah=str(random.randint(1, 100)),
            status_kepemilikan_rumah=random.choice(
                ["Milik Sendiri", "Kontrak", "Menumpang"]
            ),
            luas_lantai_m2=random.randint(20, 200),
            dinding_rumah=random.choice(["Bata", "Kayu", "Triplek"]),
            lantai_rumah=random.choice(["Keramik", "Semen", "Tanah"]),
            atap_rumah=random.choice(["Genteng", "Asbes", "Seng"]),
            status_kepemilikan_lahan_rumah=random.choice(
                ["Milik Sendiri", "Warisan", "Sewa"]
            ),
            luas_lahan_rumah_m2=random.randint(50, 500),
            penerima_bantuan=random.choice(["PKH", "BPNT", "BLT", None]),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for _ in range(n)
    ]
    session.add_all(keluargas)
    await session.commit()


async def seed_penduduks(session: AsyncSession, n=50):
    result = await session.execute(select(Keluarga.id))
    keluarga_ids = [row[0] for row in result.fetchall()]

    penduduks = [
        Penduduk(
            keluarga_id=random.choice(keluarga_ids),
            urutan_nik=random.randint(1, 10),
            nik=str(faker.unique.random_number(digits=16)),
            nama_lengkap=faker.name(),
            jenis_kelamin=random.choice(["L", "P"]),
            tempat_lahir=faker.city(),
            tanggal_lahir=faker.date_of_birth(minimum_age=1, maximum_age=90),
            agama=random.choice(["Islam", "Kristen", "Hindu", "Budha"]),
            status_pernikahan=random.choice(["Kawin", "Belum Kawin"]),
            duda_janda=random.choice([None, "Duda", "Janda"]),
            golongan_darah=random.choice(["A", "B", "AB", "O"]),
            pekerjaan=random.choice(
                ["Petani", "Pedagang", "PNS", "Wiraswasta"]
            ),
            nama_ayah=faker.name_male(),
            nama_ibu=faker.name_female(),
            hubungan_dalam_keluarga=random.choice(
                ["Kepala Keluarga", "Istri", "Anak"]
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for _ in range(n)
    ]
    session.add_all(penduduks)
    await session.commit()


async def seed_aset_keluargas(session: AsyncSession, n=30):
    result = await session.execute(select(Keluarga.id))
    keluarga_ids = [row[0] for row in result.fetchall()]

    aset_list = [
        AsetKeluarga(
            keluarga_id=random.choice(keluarga_ids),
            penguasaan_aset_tanah=random.choice(["Ya", "Tidak"]),
            aset_sarana_transportasi_umum=random.choice(
                ["Motor", "Mobil", "Sepeda"]
            ),
            aset_sarana_produksi=random.choice(
                ["Traktor", "Mesin Jahit", None]
            ),
            aset_lainnya=random.choice(["HP", "Laptop", "TV"]),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for _ in range(n)
    ]
    session.add_all(aset_list)
    await session.commit()


async def seed_pendidikans(session):
    penduduks = await session.execute(select(Penduduk))
    penduduks = penduduks.scalars().all()

    for penduduk in penduduks:
        pendidikan = Pendidikan(
            penduduk_id=penduduk.id,
            pendidikan_terakhir=random.choice(
                ["SD", "SMP", "SMA", "S1", "S2"]),
            pendidikan_sedang_ditempuh=random.choice(
                ["Tidak Sekolah", "SD", "SMP", "SMA", "S1", "S2", None]),
        )
        session.add(pendidikan)
    await session.commit()


async def seed_kesehatans(session):
    penduduks = await session.execute(select(Penduduk))
    penduduks = penduduks.scalars().all()

    for penduduk in penduduks:
        # cek apakah sudah ada data kesehatan
        exists = await session.execute(
            select(Kesehatan).where(Kesehatan.penduduk_id == penduduk.id)
        )
        if exists.scalar_one_or_none():
            continue  # skip biar ga duplikat

        kesehatan = Kesehatan(
            penduduk_id=penduduk.id,
            jaminan_sosial_ketenagakerjaan=random.choice(["BPJS TK", None]),
            jaminan_sosial_kesehatan=random.choice(["BPJS Kesehatan", None]),
            penyakit_sedang_diderita=random.choice(
                ["Batuk", "Demam", "Diabetes", None]),
            penyakit_kelainan=random.choice(["Hipertensi", "Diabetes", None]),
            cacat_fisik=random.choice(["Tunanetra", "Tuli", None]),
            cacat_mental=random.choice(["Depresi", None]),
            ibu_hamil_melahirkan=random.choice([True, False]),
            kualitas_ibu_hamil=random.choice(["Baik", "Kurang", None]),
            tempat_persalinan=random.choice(["RS", "Puskesmas", None]),
            pertolongan_persalinan=random.choice(["Bidan", "Dokter", None]),
            kualitas_bayi=random.choice(["Baik", "Kurang", None]),
            cakupan_imunisasi=random.choice(["Lengkap", "Tidak Lengkap"]),
            status_gizi_balita=random.choice(["Baik", "Kurang", None]),
            perilaku_hidup_bersih=random.choice(["Baik", "Kurang", None]),
            pola_makan=random.choice(["3x sehari", "Tidak Teratur"]),
            kebiasaan_berobat=random.choice(
                ["Puskesmas", "RS", "Klinik", None]),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(kesehatan)

    await session.commit()


async def seed_lahan_komoditas(session: AsyncSession, n=20):
    result = await session.execute(select(Keluarga.id))
    keluarga_ids = [row[0] for row in result.fetchall()]

    lahan_list = [
        LahanKomoditas(
            keluarga_id=random.choice(keluarga_ids),
            kategori=random.choice(
                ["Tanaman Pangan", "Perkebunan", "Ternak", "Perikanan"]
            ),
            memiliki=random.choice([True, False]),
            luas_lahan_are=random.randint(5, 100),
            jenis_komoditas=random.choice(["Padi", "Jagung", "Sapi", "Ikan"]),
            produksi=random.randint(100, 10000),
            satuan_produksi=random.choice(["Kg", "Ton", "Ekor"]),
            nilai_produksi=random.randint(1_000_000, 50_000_000),
            pemasaran=random.choice(["Lokal", "Ekspor"]),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for _ in range(n)
    ]
    session.add_all(lahan_list)
    await session.commit()


async def seed_pendataans(session: AsyncSession, n=15):
    result = await session.execute(select(Penduduk.id))
    penduduk_ids = [row[0] for row in result.fetchall()]

    pendataans = [
        Pendataan(
            penduduk_id=random.choice(penduduk_ids),
            completion_time=datetime.now(),
            pendata=faker.name(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for _ in range(n)
    ]
    session.add_all(pendataans)
    await session.commit()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_users(session)
        await seed_keluargas(session)
        await seed_penduduks(session)
        await seed_aset_keluargas(session)
        await seed_pendidikans(session)
        await seed_kesehatans(session)
        await seed_lahan_komoditas(session)
        await seed_pendataans(session)

    print("✅ Dummy data berhasil dimasukkan!")


if __name__ == "__main__":
    asyncio.run(main())
