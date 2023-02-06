# built-ins
import asyncio
import os
from getpass import getpass

# installed modules
from aiohttp import ClientSession

# local modules
from aiohttp_extensions import authenticate, deauth
from log import create_logger
from pdf_writer import write_pdfs
from tasks import get_profile_tasks, get_validation_tasks


def get_resume_count() -> int:
    """
    Request the number of valid resumes from the user

    Return the provided resume_count as an int or fallback to default value if input cannot be converted to int 
    """

    resume_count = input("Input the max number of resumes: ").strip()

    try:
        resume_count = int(resume_count)
    except ValueError:
        print("Valid number not provided, falling back to default value (7017)")
        resume_count = 7017

    return resume_count


async def main() -> None:

    login_url = "https://www.roadtechs.com/bbclient/login.php"
    profile_url = "https://www.roadtechs.com/bbclient/profile_print.php"

    # Prompt user for login information
    username = input("Please type your username: ")
    password = getpass("Please type your password (Output will remain blank as you type for privacy): ")

    # Get the max resume count to be downloaded
    # Number of resumes constantly changes - best to request from the user than to hardcode
    # Could eventually grab it directly from the site
    resume_count = get_resume_count()

    # Set up a semaphore to prevent overloading the server with requests
    semaphore = asyncio.BoundedSemaphore(100)

    # Set destination folder for PDF resumes
    destination_folder = f"{os.path.dirname(__file__)}/resumes"

    # Create a logger
    logger = create_logger()

    async with ClientSession() as session:

        try:

            # Authenticate the ClientSession with username and password provided above
            response = await authenticate(session, login_url, username, password)
            logger.info(str(response))

            # Get async tasks and run to retrieve all profiles
            profile_tasks = get_profile_tasks(profile_url, session, resume_count, semaphore)
            responses = await asyncio.gather(*profile_tasks)

            # Get async validation tasks and run to validate profiles
            validation_tasks = get_validation_tasks(responses)
            validations = await asyncio.gather(*validation_tasks)

            # Request and validation loop until valid_count == resume_count
            # Initial set of validations
            valid_count = validations.count(True)
            start_profile = resume_count
            end_profile = resume_count + (resume_count - valid_count) + 1

            logger.info(f"Valid resumes found: {valid_count}")

            # For testing/validation/logging
            logger.info(f"Variables: {valid_count=}, {start_profile=}, {end_profile=}")

            # Need to write only valid resumes to PDF files
            # Do this for the initial set of responses, then again below for each request-validation loop
            await write_pdfs(responses, validations, destination_folder)

            # All other validations
            # Add second while condition to break if we're risking an infinite loop
            while (valid_count < resume_count) and (end_profile < 5*resume_count):
                
                logger.info(f"Valid resumes found: {valid_count}")
                logger.info(f"Fetching profiles {start_profile} through {end_profile}")

                # Get profile tasks and run
                profile_tasks = get_profile_tasks(profile_url, session, end_profile, semaphore, start_profile)
                responses = await asyncio.gather(*profile_tasks)

                # Get validation tasks and run
                validation_tasks = get_validation_tasks(responses)
                validations = await asyncio.gather(*validation_tasks)

                valid_count += validations.count(True)
                start_profile = end_profile
                end_profile += (resume_count - valid_count)

                # For testing/validation/logging
                logger.info(f"Variables: {valid_count=}, {start_profile=}, {end_profile=}")

                # Write valid resumes again
                await write_pdfs(responses, validations, destination_folder)

        except:

            # Catch any exceptions and log them to console and log file
            issue = f"exception occured\n"
            issue += "---------------------------------------------------------------------------------"
            logger.exception(issue)

        finally:

            # Put this in finally block to avoid leaving an open session
            # Deauthorize and close the session
            await deauth(session)
            await session.close()
    
    input("Press any key to exit...")


if __name__ == "__main__":

    asyncio.run(main())